#!/bin/bash
set -e

psql -U postgres -c "CREATE DATABASE councilmatic"
psql -U postgres -c "CREATE USER councilmatic PASSWORD 'councilmatic'"
