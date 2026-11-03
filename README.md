<h1 align="center">AGENTS.md</h1>

<p align="center">
  Instructions for coding agents and ChatGPT.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-EUPL%201.2-6366f1?style=flat-square" alt="License: EUPL 1.2"></a>
</p>

<p align="center">
  <a href="AGENTS.md"><strong>AGENTS.md</strong></a>
  &nbsp;·&nbsp;
  <a href="CHATGPT.md"><strong>CHATGPT.md</strong></a>
</p>

Build `AGENTS.md` from complete section sources and small, explicit patches. Each profile selects variants and optional settings for a particular use. [CHATGPT.md](CHATGPT.md) remains an independently maintained instruction document.

Requires Python 3.11 or newer; the generator uses only the standard library. Run with [uv](https://docs.astral.sh/uv/) or an installed compatible Python interpreter.

```sh
# Preview the current instructions on stdout.
uv run scripts/build.py --profile current

# Regenerate the tracked result.
uv run scripts/build.py --profile current --output AGENTS.md

# Select a different preference and address, and write elsewhere.
uv run scripts/build.py \
  --profile python-existing \
  --address "선생님" \
  --output /path/to/project/AGENTS.md
```

`--profile` is required and takes a name such as `current`, resolved as `profiles/current.toml` in this repository. Sources, variants, and profiles are resolved relative to the generator's repository, regardless of the working directory. `--output` is relative to the caller's working directory unless given an absolute path.

Without `--output`, the completed document is written to stdout. Output uses UTF-8 with LF newlines. The destination's parent directory must already exist. The destination is replaced only after the complete build succeeds, so input or patch errors leave an existing destination unchanged. Output cannot overwrite `base.toml` or files inside `sections/`, `variants/`, `profiles/`, or `scripts/`.

| Source | Responsibility |
| --- | --- |
| [base.toml](base.toml) | Section names and output order |
| [sections/](sections/) | One complete tagged Markdown document per section |
| [variants/](variants/) | Local changes inside sections |
| [profiles/](profiles/) | Selected variants and settings |
| [scripts/build.py](scripts/build.py) | Composition, address substitution, and output |
| [AGENTS.md](AGENTS.md) | Tracked output generated with the `current` profile |

Edit the sources and regenerate `AGENTS.md`; do not maintain the generated file separately. Section names in `base.toml` resolve to `sections/{name}.md`. Keep each section's outer tags and its existing internal structure. The `current` profile applies no patches and preserves the current instructions with the default address.

A variant is a TOML file containing one or more `[[patches]]` entries. For example, [variants/python-existing.toml](variants/python-existing.toml) changes only the Python tool preference:

```toml
[[patches]]
section = "environment"
before = '''
        Use uv to run Python and manage environments.
'''
after = '''
        Use the project's existing Python tooling and environment manager.
'''
```

`section` identifies the base section; `before` is a nonempty exact match, including indentation and newlines; `after` supplies the replacement. Use multiline literal strings as shown to preserve the text without escaping. Delete a passage with `after = ""`. Insert content by retaining an existing anchor passage in `after` and adding the new content beside it. Patch only the necessary passage inside the section. There is no section-level replacement or deletion operation: outer section tags must remain unchanged and the body cannot become empty. The example is a selectable preference, not automatic device detection.

All patch locations are resolved against the unchanged section sources, before address substitution. Each `before` must match exactly once; missing or ambiguous matches fail the build. Disjoint patches in the same section compose, while overlapping matched ranges fail, even if the overlap is only shared context. Narrow the selected text or combine related changes when their ranges overlap. Profile order is not overwrite precedence, and patches cannot depend on another patch's result.

When matching base text changes, review its variants; unrelated base changes flow into every profile. Keep connected conditions and their consequences consistent when editing a passage.

A profile selects variant names, resolved as `variants/{name}.toml`, and may override the address:

```toml
variants = ["python-existing"]

[settings]
address = "선생님"
```

The address is resolved as `--address`, then profile `settings.address`, then the script default `마스터`. It must be a nonempty single-line string. Only the reserved `{settings.address}` token is substituted, once; existing placeholders such as `{stage}` and proposal-template braces remain literal.

The accepted fields are `sections` in the base, `variants` and optional `settings.address` in a profile, and `section`, `before`, and `after` in each patch. Section, variant, and profile names start with an ASCII letter and contain only ASCII letters, digits, `_`, or `-`. Unknown fields, invalid names, and missing files fail the build rather than silently changing the selected instructions.
