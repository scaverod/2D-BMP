# Optimizing the two-dimensional bandwidth problem under the maximum norm using exact and heuristic approaches <a href="https://doi.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/1/11/DOI_logo.svg" alt="DOI" width="20"/></a> <a href="https://doi.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e8/Zenodo-gradient-square.svg" alt="DOI" width="60"/></a>

<!-- Load Material Symbols Outlined for the mail icon -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=mail" />


## Abstract
Paper under review. To be added upon acceptance.

## Authors

- Sergio Cavero Díaz<sup>1</sup>   <a href="mailto:sergio.cavero@urjc.es" aria-label="Email Sergio"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg" alt="email" width="20" style="vertical-align:middle;"/></a>
    <a href="https://orcid.org/0000-0002-5258-5915"><img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID" width="20" style="vertical-align:middle;"/></a>


- Eduardo G. Pardo<sup>1</sup> *  <a href="mailto:eduardo.pardo@urjc.es" aria-label="Email Eduardo"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg" alt="email" width="20" style="vertical-align:middle;"/></a>
    <a href="https://orcid.org/0000-0002-6247-5269"><img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID" width="20" style="vertical-align:middle;"/></a>



- Eduardo Rodriguez-Tello<sup>2</sup>  <a href="mailto:ertello@cinvestav.mx" aria-label="Email Eduardo R-T"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg" alt="email" width="20" style="vertical-align:middle;"/></a>
    <a href="https://orcid.org/0000-0002-0333-0633"><img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID" width="20" style="vertical-align:middle;"/></a>



- Eric Monfroy<sup>3</sup>  <a href="mailto:eric.monfroy@univ-angers.fr" aria-label="Email Eric"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg" alt="email" width="20" style="vertical-align:middle;"/></a>
    <a href="https://orcid.org/0000-0001-7970-1368"><img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID" width="20" style="vertical-align:middle;"/></a>

    

- Claudia Vasconcellos-Gaete<sup>3</sup>   <a href="mailto:claudia.vasconcellos@univ-angers.fr" aria-label="Email Claudia"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg" alt="email" width="20" style="vertical-align:middle;"/></a>
    <a href="https://orcid.org/0000-0001-9487-0573"><img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID" width="20" style="vertical-align:middle;"/></a>



### Affiliations

1. Departamento de Informática y Estadística, Universidad Rey Juan Carlos — C. Tulipán, s/n, Móstoles, 28933, Madrid, Spain

2. Cinvestav, Unidad Tamaulipas — Km. 5.5 Carretera Victoria - Soto La Marina, Victoria, 87130, Tamaulipas, Mexico

3. LERIA, Université d'Angers — 2 Bd de Lavoisier, Angers, 49000, France

\*Corresponding author.

## Datasets

Instances are categorized in different datasets inside the `instances` folder. All instances are either from the https://archive.ics.uci.edu/ml/index.php, the Harwell-Boeing Sparse Matrix Collection, or generated based on graph families described in the paper.

### Instance format

Each instance is encoded as a plain text file representing a graph:
- The first line contains the number of vertices `n` and edges `m`.
- Each subsequent line contains a pair of integers `u v` representing an edge between vertex `u` and vertex `v`.
- Vertices are indexed from 0 to n-1.

Example:
```

10 15
0 1
0 2
1 3
...

````

## CBMA


Execution of the program can be done via the command line.

Example 1: execute default experiment with the default set of instances

```bash
java -jar target/CBMA.jar 
```

Example 2: execute using a different set of instances, located inside the `newinstances` folder.

```bash
java -jar target/CBMA.jar --instances.path.default=newinstances
```

## MDO: A constraint-based solution for the 2DBMP running inside a dichotomic optimization procedure.

### Pre-requisites

1. Python 3.10+
2. [PyCSP3](https://github.com/xcsp3team/pycsp3)
    ```bash
    sudo pip3 install pycsp3
    sudo apt-get install openjdk-11-jdk
    ```
    or
    ```bash
    sudo pip3 install --upgrade pycsp3
    ```

### Running the code

    ```bash
    python3 matrix_bandwidth.py -lb=<lower> -ub=<upper> -data=<instance> -parser=mtx_parser.py
    ```

## Cite

Consider citing our paper if used in your own work:

### DOI

<https://doi.org/XXXXXXX>

### Bibtex

```bibtex
@article{cavero2025heuristic,
  title={Heuristic and Exact Approaches for the Two-Dimensional Bandwidth Problem},
  author={Cavero, Sergio and Pardo, Eduardo G. and Rodriguez-Tello, Eduardo and Monfroy, Eric and Vasconcellos-Gaete, Claudia},
  journal={XXXXXX},
  year={202X},
  doi={XXXXXXX}
}
```



## Powered by MORK (Metaheuristic Optimization framewoRK)
| ![Mork logo](https://user-images.githubusercontent.com/55482385/233611563-4f5c91f2-af36-4437-a4b5-572b6655487a.svg) | Mork is a Java framework for easily solving hard optimization problems. You can [create a project](https://generator.mork-optimization.com/) and try the framework in under one minute. See the [documentation](https://docs.mork-optimization.com/en/latest/) or the [source code](https://github.com/mork-optimization/mork). |
|--|--|
