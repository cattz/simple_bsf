# Simple Build Scripts Framework

This is a simplified version of [Build Scripts Framework](https://github.com/cattz/build_scripts_framework)
The idea is to run build scripts that can be configured via a yaml file like this:

```yaml
	release:
		config:
			artifact_repo: promotion-repo
		tasks:
			publish:
				config:
					artifact_repo: foo # Overrides the release level config value
				steps:
					- do_something
					- publish
			another_task:
				steps:
					- promote:
					- send_email:
					- 	recipient: group@mycompany.com
```
We can choose what runner/task we want to execute from the command line. All steps in the task will be run sequentially:

```
> ./bsf release promote
> Running release:promote
----------------------------------------------------
Running step {'promote': {'repo': 'promotion-repo'}}
ReleaseWorker: Promoting to promotion-repo
----------------------------------------------------
Running step {'send_email': {'recipient': 'group@mycompany.com'}}
Sending email to group@mycompany.com
```
