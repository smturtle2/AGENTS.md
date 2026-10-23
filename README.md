# AGENTS.md

Instructions for coding agents that reason independently and work through explicit proposals, approval, and review.

Agents are expected to compare approaches, explain the basis of their decisions, and address underlying causes across the approved scope.

[Read the full instructions](AGENTS.md)

## Workflow

- **Discuss first.** The default mode is DISCUSSION. The agent develops a complete proposal, and the proposed work begins only after explicit approval.
- **Research when needed.** The agent enters RESEARCH to resolve questions about the problem or an approach. It summarizes its findings and remaining uncertainty, then returns to the activity that needed the research.
- **Review the complete result.** Implementation includes REVIEW of the whole current result. Completed work is reported, and the conversation returns to DISCUSSION.
- **Approve testing separately.** Testing is optional. It requires its own approved proposal after the implementation passes review.

Execution stops at the user's request or when continuing would exceed authorization. Mode changes are announced as `[MODE SWITCH: <MODE>]`.

## Contents

| Section | Covers |
| --- | --- |
| `<workflow>` | Activity modes, approval boundaries, execution, and completion. |
| `<development>` | Developing and comparing approaches, research, responsibility boundaries, and implementation and review criteria. |
| `<communication>` | Evidence and uncertainty, proposal format, mode announcements, and dialog behavior. |
| `<delegation>` | Assignment scope, follow-up rules, and the `Default` and `Advisor` types. |
| `<environment>` | Artifact organization, cleanup, Python, Git, and privileged commands. |

## License

Licensed under the [European Union Public Licence 1.2](LICENSE).
