# Setting up LaminR

This guide provides more detailed instructions for how to set up **{laminr}**.

## Installing **{laminr}**

The **{laminr}** package can be installed from CRAN:

```r
install.packages("laminr")
```

### Additional packages

Some functionality in **{laminr}** requires additional packages.
To install all suggested dependencies use:

```r
install.packages("laminr", dependencies = TRUE)
```

If you choose not to install all additional packages you will be prompted to do so as needed.

### Installing the development version

The current development version of **{laminr}** can be installed from GitHub using:

```r
if (!requireNamespace("laminr", quietly = TRUE)) {
  install.packages("remotes")
}
remotes::install_github("laminlabs/laminr")
```

This version may have bug fixes and new features but could also be unstable so is not recommended for most users.

## Installing Python **lamindb**

Using **{laminr}** requires the Python **lamindb** package to be available.

### Using the included Python environment

The recommended way to use **{laminr}** is to connect to the included `r-lamindb` Python environment.
This can be created using:

```r
laminr::install_lamindb()
```

This should be run before the first time you load the **{laminr}** library.
The **{reticulate}** package will then be told to use this environment when **{laminr}** is loaded.

#### Adding additional packages

If you want to add additional packages to the environment, these can be specified using the `extra_packages` argument.
For example, to add the **bionty** package:

```r
laminr::install_lamindb(extra_packages = "bionty")
```

Example of Python packages providing additional registries that may be used in your instance:

- [**bionty**](https://docs.lamin.ai/bionty) - Basic biological entities, coupled to public ontologies
- [**clinicore**](https://docs.lamin.ai/clinicore) - Basic clinical entities
- [**omop**](https://omop.lamin.ai/) - OMOP Common Data Model
- [**wetlab**](https://docs.lamin.ai/wetlab) - Basic wetlab entities

Installing additional Python packages also be useful if you want to use another R package which expects a particular Python module to be installed.

#### Adding **lamindb** to another environment

To install **lamindb** into another environment, set the `envname` argument:

```r
laminr::install_lamindb(envname = "your-env")
```

Be aware that there may be dependency conflicts with packages already installed in the environment and installing **lamindb** may cause package versions to change.

### Setting the Python environment

Running `library(laminr)` will tell **{reticulate}** to use the included `r-lamindb` environment (if it has not already connected to another environment).

If you prefer to not load the whole package, and instead call functions using `laminr::`, you should tell **{reticulate}** which environment to use by running `reticulate::use_virtualenv("r-lamindb")`.

#### Using another environment

In some cases you may prefer to use another Python environment.
This may be the case if you use another R package which requires a Python module or if you are managing your own Python environment.

Specifying another Python environment to use should be done **_before_** loading **{laminr}** (or **{reticulate}**) using one of these methods:

- Loading another R package that sets the Python environment
- Using `reticulate::use_virtualenv()`, `reticulate::use_condaenv()` or `reticulate::use_python()`
- Setting the `RETICULATE_PYTHON` or `RETICULATE_PYTHON_ENV` environment variables

Details of the current Python environment can be viewed using `reticulate::py_config()`.
For more information about setting the active Python environment see `vignette("versions", package = "reticulate")` (also [available here](https://rstudio.github.io/reticulate/articles/versions.html)).

## Logging in to LaminDB

If you have not used LaminDB before you will need to login to access public instances.
To do this you will need a user API key which you can get by logging in to [LaminHub](https://lamin.ai/dashboard) and going to your user settings.

You can then login with:

```r
laminr::lamin_login(api_key = "your_api_key")
```

### Switching users

If you have already given an API key for a user you can log in as them by giving the user name:

```r
laminr::lamin_login(user = "user_handle")
```

## Setting a default instance

Using `import_module("lamindb")` will connect to the current default LaminDB instance.
The default instance can be set using:

```
laminr::lamin_connect("<owner>/<name>")
```

Note that this must be called before attempting to connect to a default instance and cannot be changed once the default instance is connected without first calling `lamin_disconnect()`.
