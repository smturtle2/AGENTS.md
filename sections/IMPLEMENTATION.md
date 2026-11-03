<IMPLEMENTATION>
    REPEAT
        Produce a coherent result that meets requirements and solves the underlying problem across the affected scope.
        Examine responsibility boundaries.
        IF a responsibility is fragmented THEN
            Consolidate it under a clear owner.
        IF concerns change for different reasons THEN
            Separate them.
            Do not merge them solely because their code is similar.
        IF correcting the current approach can resolve the cause AND meet requirements across the affected scope THEN
            Correct it.
        ELSE
            Replace it and correct the structure.
        Do not preserve the underlying problem through local patches or case-specific rules.

        IF the change's complexity, impact, or remaining uncertainty warrants review
           OR a required review has not passed THEN
            Follow REVIEW.
            IF the review has not passed THEN
                Follow RESEARCH.
    UNTIL no required changes remain AND any required review has passed
       OR execution must stop.
</IMPLEMENTATION>
