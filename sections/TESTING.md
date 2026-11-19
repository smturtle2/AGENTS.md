<TESTING>
    Begin approved testing only after implementation is complete.
    Preserve the approved cases, execution conditions, and expected outcomes with the project's test assets.
    Follow the project's test structure and execution workflow.
    Reuse existing tests for the approved cases they cover.
    IF the approved plan has coverage gaps THEN
        Adapt or add tests to cover those gaps.
    Provide setup, data, cleanup, and run instructions.

    Execute the complete approved plan against the completed implementation.
    Compare observations with the planned criteria.
    Distinguish implementation defects, test defects, and unevaluated cases.

    WHILE failures require correction:
        Follow RESEARCH.
        IF execution must stop THEN
            BREAK
        ELSE IF the correction concerns implementation THEN
            Follow IMPLEMENTATION.
        ELSE
            Correct the test code or setup.
        Rerun affected tests and reassess the results.

    Record results, remaining gaps, and how to reproduce them.
</TESTING>
