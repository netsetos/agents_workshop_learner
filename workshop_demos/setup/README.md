# Setup and reusable functions

Run these files with the same interpreter as the demos. They replace repeated shell setup without hiding the lesson's experiment.

| File or helper | Why it exists | When to use it |
|---|---|---|
| `bootstrap.py` | Installs `workshop_helpers` into the selected interpreter; preserves local settings | First setup, or after changing interpreters |
| `install_dependencies.py` | Installs a chosen set of the kit's own requirements using that same interpreter | When the operator/local lane dependencies are missing |
| `authenticate.py` | Refreshes Python ADC through interactive gcloud login | On an ADC reauthentication error |
| `check_setup.py` | Checks Firestore, uploads access and serving API configuration | Before lessons on an already deployed lane |
| `update_kit.py` | Updates the currently tracked Git branch without discarding edits | For an authorized kit refresh |
| `start_new_session.py` | Archives the active pointer after cleanup, retaining all evidence | To restart a lesson from its first example |
| `recover_session.py` | Verifies a stopped process before removing its leftover lock | After a terminated IDE process left a lock |
| `DemoSession` | Makes separate Run/Debug launches share one lesson's identity and progress | Every demo entry point |
| `session.set_environment(**values)` | Shares nonsecret values with later Python and command checkpoints | When a Python example changes a lesson variable |
| `session.service_environment(service, keys)` | Reads literal settings from the actual serving revision as JSON | Before comparing the API's retrieval/embedding configuration |
| `session.command(args)` | Executes a CLI argument list with visible output and real exit status | Make, gcloud and existing kit scripts |
| `session.shell(code)` | Preserves reviewed variables and functions across Bash workflows | Multi-command examples from the main HTML |
| `session.pin_vector()` / `restore_backend()` | Saves and restores the actual prior tenant pin | Lessons that temporarily demonstrate the vector lane |
| `session.start_local_service()` / `stop_local_service()` | Owns a local process without holding an IDE run open indefinitely | Module 1's local chat experiment |
| `workshop_helpers.reconciliation` | Explains decisions using the kit's real planner | Lesson 4.4's offline queued/default/known-bytes examples |

`config/settings.example.json` documents the accepted configuration keys. Bootstrap creates the ignored `settings.local.json`; `WORKSHOP_DEMO_CONFIG` can select a different local file if needed. `kit_root: "auto"` resolves relative to the installed helper, independent of the IDE working directory. The selected interpreter's directory is placed first on PATH for child commands.

Setup does not create an index, invent an endpoint ID or renew credentials invisibly. A lesson either discovers its resource from the serving configuration or runs the real kit provisioning step that introduces it. Split traffic requires an explicit decision because one environment snapshot cannot describe two serving revisions.

The original small helper modules (`config`, `auth`, `discovery`, `api`, `artifacts`, `kit`, `context`, `reconciliation`) provide reusable operations. `DemoSession` adds cross-file state, ordered attempts and the CLI bridge used by the full course. Native examples execute in the lesson's `demonstrate` function so their educational logic remains visible to the debugger.
