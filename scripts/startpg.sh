#!/bin/sh


docker start sh-postgres || docker run --name sh-postgres -e POSTGRES_PASSWORD=password -d -p "5132:5432" postgres
