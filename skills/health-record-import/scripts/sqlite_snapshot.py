"""Read one owner-bound SQLite snapshot and fingerprint logical contents, including WAL."""
import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3


def fingerprint(connection):
    """Versioned logical digest; call inside a transaction, never hash a live DB blob."""
    digest = hashlib.sha256(b'health-ledger-logical-v1\0')
    for statement in connection.iterdump():
        digest.update(statement.encode('utf-8'))
        digest.update(b'\0')
    return digest.hexdigest()


def check_owner(connection, record_id):
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError('Explicit archive record_id required')
    owners = {row[0] for row in connection.execute('SELECT DISTINCT record_id FROM imports')}
    if owners != {record_id}:
        raise ValueError('Database owner mismatch or uninitialized owner')


@contextmanager
def snapshot(db, record_id):
    # as_uri quotes spaces, # and ? rather than interpreting them as SQLite URI options.
    connection = sqlite3.connect(Path(db).resolve().as_uri() + '?mode=ro', uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute('BEGIN')
        if connection.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Database integrity failed')
        check_owner(connection, record_id)
        yield connection
    finally:
        connection.close()


def current_fingerprint(db, record_id):
    with snapshot(db, record_id) as connection:
        return fingerprint(connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True)
    parser.add_argument('--record-id', required=True)
    args = parser.parse_args()
    print(json.dumps({'ledger_fingerprint': current_fingerprint(args.db, args.record_id),
                      'fingerprint_format': 'health-ledger-logical-v1'}))
