### Development Workflow (using uv)

The project uses `uv` for package management. Always use uv to call tools and scripts!

# CODING CONVENTIONS

* Make sure to write documentation for each method/function. Make sure to update the documentation if the function signature changes.
* Write short, optimized code rather than lengthy verbose spaghetti.
* Generate functional and vectorized code whenever possible avoiding loops.
* Do not create nested loops in your code unless absolutely necessary!
* When creating CLI tools, use typer
* When dealing with paths prefer pathlib over os.path
* Prefer asynchronous code over synchronous code.
* Prefer using `asyncio` over `threading` or `multiprocessing` for concurrency.

* Use python 3.12+ typing hints whenever possible.
* Avoid duplicated code!

# Documentation
Output docstrings in the following format:
```
def function_name(arg1: arg1_type, arg2: arg2_type) -> return_type:
    """
    Description of the function.

    :param arg1: Description of the first argument.
    :param arg2: Description of the second argument.
    :return: Description of the return value.
    """
    ...
```

### Testing & Code Quality

Use Ruff for linting and Black-compatible formatting: 99-character lines, double quotes, and spaces. Preserve the docstring format above.

Run these read-only checks in parallel, only on modified Python files:
```bash
uv run ruff check --line-length 99 $files
uv run ruff format --check --line-length 99 $files
uv run mypy $files
uv run basedpyright $files
```

Apply lint fixes before formatting; run these commands sequentially:
```bash
uv run ruff check --fix --line-length 99 $files
uv run ruff format --line-length 99 $files
```
