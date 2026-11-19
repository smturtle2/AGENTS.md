<environment>
    IF creating or revising artifacts THEN
        Follow the existing workspace organization.
        Keep related files together and make the current result easy to identify.

        IF the existing and requested artifacts must remain usable independently THEN
            Keep them separate and make their purposes distinguishable.
        ELSE IF an existing artifact already serves the requested purpose THEN
            Prefer updating it over creating a redundant copy.
        ELSE
            Place the new artifact with the related work.

        Keep temporary work separate from maintained artifacts.

    IF writing prose in files THEN
        Use line breaks only for document structure, keeping each sentence on one physical line.

    BEFORE handoff or completion:
        Clean up your own unneeded leftovers.
        Preserve unrelated work.

    IF using Python THEN
        Use uv to run Python and manage environments.

        IF doing project work THEN
            Respect the project's Python version and dependency setup.
            Change that setup only when required by the task.
        ELSE IF doing incidental work THEN
            Isolate temporary dependencies from the project and system Python.

    IF working with Git THEN
        Work on the current branch by default.
        IF creating a branch directly, through a worktree, or through another workflow THEN
            Proceed only on the user's explicit request.

        IF committing THEN
            Review the full working tree and staged changes.
            Include only intended work.

            Use Conventional Commits:
                type[(scope)][!]: description

            Keep the subject concise.
            Include necessary rationale or breaking-change details in the body.

    IF issuing your own authorized privileged commands
       AND the execution shell's EUID is not 0 THEN
        IF no persistent elevation shell has been started
           OR the existing shell has exited THEN
            Start `run0 --empower --pty` without a command in a PTY-enabled session.
            Keep its session ID.
        ELSE
            Reuse the existing shell.

        The shell retains the invoking user's UID.
        Run commands requiring UID 0 through `run0` inside that shell.

        Send commands through `write_stdin`.
        Preserve each command's required execution context.

        IF execution fails THEN
            Diagnose the failure and resolve routine invocation issues.

            IF blocked THEN
                Explain the cause.

            Do not silently switch elevation methods.

    IF generating scripts that need privilege handling THEN
        Choose that handling from their intended runtime and requirements.
        Do not carry your own execution policy into the generated scripts.
</environment>
