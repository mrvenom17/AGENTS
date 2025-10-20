import click
from core.rules import load_rules_from_dir
from core.parser import match_intent, render_command

@click.command()
@click.argument('intent', nargs=-1)
@click.option('--dry-run', is_flag=True, default=True, help="Show command without executing (default)")
def main(intent, dry_run):
    intent_str = " ".join(intent)
    if not intent_str:
        click.echo("❌ Error: Please provide an intent (e.g., 'op-shell restart nginx on staging')")
        return

    try:
        rules = load_rules_from_dir()
    except Exception as e:
        click.echo(f"❌ Failed to load rules: {e}")
        return

    result = match_intent(intent_str, rules)
    if not result:
        click.echo(f"❓ Unrecognized intent: '{intent_str}'")
        click.echo("💡 Try one of these:")
        for r in rules:
            click.echo(f"   - {r.intent} (pattern: /{r.pattern}/)")
        return

    rule, params = result
    command = render_command(rule, params)

    # Safety: block if env not allowed
    if rule.template.allowed_envs:
        env = params.get("env")
        if env not in rule.template.allowed_envs:
            click.echo(f"🚫 Environment '{env}' not allowed. Allowed: {rule.template.allowed_envs}")
            return

    click.echo("✅ Intent understood!")
    click.echo(f"📝 Description: {rule.template.description}")
    click.echo(f"💻 Command: {command}")
    if rule.template.requires_approval:
        click.echo("⚠️  Requires approval before execution.")
    click.echo("\n[DRY-RUN MODE] No action taken.")