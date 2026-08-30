# Architecture

## Request flow

```mermaid
flowchart LR
    Browser -->|HTTPS 443| DNS
    DNS --> Nginx
    Nginx -->|Loopback 8080| Moodle
    Moodle -->|Bridge network| MariaDB
```

## Trust boundaries

```mermaid
flowchart TB
    subgraph Public
      U[Users]
      D[DNS]
    end
    subgraph VPS[Ubuntu VPS]
      N[Nginx + TLS]
      subgraph Docker[Docker Compose]
        M[Moodle]
        DB[MariaDB]
        NET[mundoactivate-internal]
        M --- NET --- DB
      end
      MV[(moodle_data)]
      DV[(mariadb_data)]
    end
    U --> D --> N --> M
    M --> MV
    DB --> DV
```

## Design decisions

1. **Loopback-only Moodle binding:** the application is published on `127.0.0.1`, so only the host proxy can reach it.
2. **No database host port:** MariaDB is reachable only by containers attached to the private bridge network.
3. **Health-aware startup:** Moodle waits until MariaDB reports a healthy state.
4. **Persistent data:** application files and database state are stored in named volumes.
5. **Host-level edge:** Nginx terminates TLS and centralizes public web controls.
6. **Recoverability:** database and application data are backed up together and must be tested through isolated restores.
