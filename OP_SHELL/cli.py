# op_shell/cli.py
import click
import sys
from core.rules import load_rules_from_dir
from core.parser import match_intent, render_command
from core.executor import execute_in_sandbox, execute_on_host
from core.audit import log_event
from core.rbac import get_current_user, load_policy, is_intent_allowed
from core.rollback import record_pre_state


@click.command()
@click.argument('intent', nargs=-1)
@click.option('--dry-run', is_flag=True, help="Show command without executing (default behavior)")
@click.option('--execute', is_flag=True, help="Execute the command (in sandbox or on host)")
@click.option('--rollback', is_flag=True, help="Restore last snapshot (not implemented in Stage 3)")
def main(intent, dry_run, execute, rollback):
    # Handle rollback early (Stage 3: not implemented)
    if rollback:
        click.echo("⚠️  Rollback is not implemented in Stage 3 (manual restore only).")
        return

    intent_str = " ".join(intent).strip()
    if not intent_str:
        click.echo("❌ Error: Please provide an intent (e.g., 'op-shell restart nginx on staging')")
        sys.exit(1)

    # Load policy and user
    user = get_current_user()
    try:
        policy = load_policy()
    except Exception as e:
        click.echo(f"❌ Failed to load policy: {e}")
        sys.exit(1)

    # Load rules
    try:
        rules = load_rules_from_dir()
    except Exception as e:
        click.echo(f"❌ Failed to load rules: {e}")
        sys.exit(1)

    # Parse intent
    result = match_intent(intent_str, rules)
    if not result:
        log_event(user, intent_str, "UNMATCHED", "", "unrecognized_intent")
        click.echo(f"❓ Unrecognized intent: '{intent_str}'")
        click.echo("💡 Try one of these:")
        for r in rules:
            click.echo(f"   - {r.intent} (pattern: /{r.pattern}/)")
        sys.exit(1)

    rule, params = result
    command = render_command(rule, params)

    # 🔒 RBAC: Is user allowed to run this intent?
    if not is_intent_allowed(rule.intent, user, policy):
        log_event(user, intent_str, rule.intent, command, "rbac_denied")
        click.echo(f"🚫 Access denied. User '{user}' is not authorized to perform this action.")
        sys.exit(1)

    # 🌐 Environment check
    if rule.template.allowed_envs:
        env = params.get("env")
        if env not in rule.template.allowed_envs:
            click.echo(f"🚫 Environment '{env}' not allowed. Allowed: {rule.template.allowed_envs}")
            sys.exit(1)

    # 🔄 Record pre-exec state (for audit/rollback)
    pre_state = record_pre_state(command, params)

    # Log dry-run attempt
    log_event(user, intent_str, rule.intent, command, "dry_run", {"pre_state": pre_state})

    # ✅ Show parsed intent
    click.echo("✅ Intent understood!")
    click.echo(f"📝 Description: {rule.template.description}")
    click.echo(f"💻 Command: {command}")
    click.echo(f"👤 User: {user}")
    click.echo(f"RuleContext: {rule.template.execution_context}")

    if rule.template.requires_approval and not execute:
        click.echo("⚠️  This action requires explicit approval. Use --execute to proceed (if authorized).")

    # 🚫 If not executing, stop here
    if not execute:
        click.echo("\n[DRY-RUN MODE] Use --execute to run the command.")
        return

    # 🔐 Require approval for sensitive actions (even if RBAC allows)
    if rule.template.requires_approval:
        click.echo("\n🛡️  Approval required for this operation.")
        confirm = click.prompt("Type 'yes' to confirm execution", default='no')
        if confirm.lower() != 'yes':
            click.echo("❌ Execution aborted by user.")
            log_event(user, intent_str, rule.intent, command, "execution_aborted")
            sys.exit(0)

    # 🚀 Execute based on context
    execution_context = rule.template.execution_context
    log_event(user, intent_str, rule.intent, command, "execute_attempt", {"pre_state": pre_state})

    if execution_context == "host":
        click.echo("\n🚨 Executing ON HOST (privileged action)...")
        output = execute_on_host(command)
        status = "host_execute_success" if output is not None else "host_execute_failure"
    else:
        click.echo("\n🚀 Executing in sandbox...")
        output = execute_in_sandbox(command)
        status = "sandbox_execute_success" if output is not None else "sandbox_execute_failure"

    # 📝 Log result
    log_event(
        user,
        intent_str,
        rule.intent,
        command,
        status,
        {"output": output[:500] if output else None, "pre_state": pre_state}
    )

    if output is not None:
        click.echo("✅ Execution successful:")
        click.echo(output)
    else:
        click.echo("❌ Execution failed or was unsafe.", err=True)
        sys.exit(1)