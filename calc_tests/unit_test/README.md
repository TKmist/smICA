# smICA standalone calculation unit tests

The scripts validate selected numerical functions without starting the GUI and do
not require pytest. Run the complete set from a source checkout with:

```bash
python calc_tests/unit_test/run_all.py
```

After installing smICA, use the generated launcher:

```bash
./run_smICA --test
```

On Windows, run:

```bat
smICA.bat --test
```

Each `test_*.py` file can also be executed separately with the Python interpreter
from the smICA environment.
