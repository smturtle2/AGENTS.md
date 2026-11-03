<TESTING>
    Begin the approved testing work only after implementation is complete.
    Preserve the approved cases, execution conditions, and expected outcomes with the project's test assets.
    Reuse existing tests that cover the approved plan; develop or adapt tests where additional coverage is needed, using the project's established test structure and execution workflow.
    Provide the setup, data, cleanup, and run instructions needed to repeat them.

    Execute the complete approved plan against the completed implementation.
    Compare observed outcomes with the planned criteria.
    Distinguish implementation defects, test defects, and cases that could not be evaluated.

    WHILE failures require corrections:
        Follow RESEARCH.

        IF execution must stop THEN
            BREAK
        ELSE IF the correction concerns implementation THEN
            Follow IMPLEMENTATION.
        ELSE
            Correct the test code or setup.

        Rerun the affected tests and reassess the results.

    Record the results and remaining gaps, including the information needed to reproduce them.
</TESTING>
