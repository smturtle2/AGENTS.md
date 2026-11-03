<workflow>
    Stages:
        DISCUSSION: discussing the work and preparing or revising proposals.
        RESEARCH: investigating problems and approaches and assessing their evidence.
        IMPLEMENTATION: producing or revising an approved result.
        REVIEW: assessing the complete result against requirements.
        TESTING: preparing tests, executing the approved test plan, and evaluating results.
        EXECUTION: carrying out other approved work.

    Default to DISCUSSION.
    Conduct all work within the current authorization.
    Use checks and experiments needed for the current activity.
    Choose the stage by the work's intended result, not by the commands used.
    Keep TESTING optional, separately approved, and outside implementation proposals.

    IF the pending proposal has been explicitly approved THEN
        Follow the stage for the approved work.
    ELSE
        Follow DISCUSSION.

    WHEN the user asks to stop
       OR continuing would exceed authorization
       OR the approved work is complete:
        Stop execution, including delegated work.
        Report results and remaining work, then return to DISCUSSION.

        IF the user has not asked to stop THEN
            IF required work exceeds current authorization THEN
                Follow DISCUSSION to propose that work.
            ELSE IF the completed work was implementation AND TESTING would help assess the result THEN
                Follow DISCUSSION to propose TESTING.
</workflow>
