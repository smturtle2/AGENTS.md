<IMPLEMENTATION>
    REPEAT
        Resolve the underlying problem across the affected scope and meet the requirements as a whole.
        Do not use a fixed number for a behavioral decision unless a requirement, contract, or domain invariant fixes that exact value for every case the decision covers.
        IF a responsibility is fragmented THEN
            Consolidate it under one owner.
        IF concerns change for different reasons THEN
            Separate them even when their code is similar.

        IF correcting the current approach can resolve the cause AND meet requirements across the affected scope THEN
            Correct it.
        ELSE
            Replace the approach and correct the structure.

        IF complexity, impact, or remaining uncertainty warrants review
           OR a required review has not passed THEN
            Follow REVIEW.
            IF the review has not passed THEN
                Follow RESEARCH.
    UNTIL no required changes remain AND any required review has passed
       OR execution must stop.
</IMPLEMENTATION>
