# Medicine

This project fetches Icelands medicine pricing over time for the past few years using their [`website`](https://www.lyfjastofnun.is/verd-og-greidsluthatttaka/lyfjaverdskra/).

It aims to use the [`ngods stack`](https://github.com/zsvoboda/ngods-stocks) as an end to end product, this is a hobby project made over time.

This starter demonstrates using Python alongside a medium-sized dbt project. It uses dbt, [`dagster-dbt`](https://docs.dagster.io/_apidocs/libraries/dagster-dbt), and [DuckDB](https://duckdb.org/).

_New to Dagster? Learn what Dagster is in [Dagster's hands-on Tutorials](https://docs.dagster.io/tutorial) or learn using dbt with Dagster in the [dbt + Dagster tutorial](https://docs.dagster.io/integrations/dbt/using-dbt-with-dagster)._

## Getting started


### Running it locally

To install Dagster and its Python dependencies, run:

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```
dagster dev

```

Then run 
```
docker compose up
```

Which will setup the cube and minio instances.

Then navigate to the infrastructure folder and write
```
terraform apply
```

This will create the necessary buckets in your minio instance to run everything.

Alternatively, you can run ```make setup```

Open http://localhost:3000 with your browser to see the project.

## Learning more

### Changing the code locally

When developing pipelines locally, be sure to click the **Reload definition** button in the Dagster UI after you change the code. This ensures that Dagster picks up the latest changes you made.

You can reload the code using the **Deployment** page:

<details><summary>👈 Expand to view the screenshot</summary>

<p align="center">
    <img height="500" src="https://raw.githubusercontent.com/dagster-io/dagster/master/docs/next/public/images/quickstarts/basic/more-reload-code.png" />
</p>

</details>

Or from the left nav or on each job page:

<details><summary>👈 Expand to view the screenshot</summary>

<p align="center">
    <img height="500" src="https://raw.githubusercontent.com/dagster-io/dagster/master/docs/next/public/images/quickstarts/basic/more-reload-left-nav.png" />
</p>

</details>

### Using environment variables and secrets

Environment variables, which are key-value pairs configured outside your source code, allow you to dynamically modify application behavior depending on environment.

Using environment variables, you can define various configuration options for your Dagster application and securely set up secrets. For example, instead of hard-coding database credentials - which is bad practice and cumbersome for development - you can use environment variables to supply user details. This allows you to parameterize your pipeline without modifying code or insecurely storing sensitive data.

Check out [Using environment variables and secrets](https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets) for more info and examples.

### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Testing

Tests are in the `assets_dbt_python_tests` directory and you can run tests using `pytest`:

```bash
pytest assets_dbt_python_tests
```

### Infrastructure

- [Apache Iceberg](https://iceberg.apache.org) as a data storage format *TODO*
- [Trino](https://trino.io/) for federated data query *TODO*
- [dbt](https://www.getdbt.com/) for ELT 
- [Dagster](https://dagster.io/) for data orchetsration 
- [cube.dev](https://cube.dev/) for data analysis and semantic data model *TODO*
- [Metabase](https://www.metabase.com/) for self-service data visualization (dashboards) *TODO*
- [Minio](https://min.io) for local S3 storage 