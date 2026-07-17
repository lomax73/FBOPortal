"""Import dell'anagrafica clienti da un export .xlsx del gestionale.

Mapping per nome di colonna (non per posizione), così l'ordine delle
colonne nell'export può cambiare senza rompere l'import. Ogni chiave è
l'intestazione esatta usata nell'export, il valore è il nome del campo
su Cliente.
"""

import openpyxl

COLUMN_TO_FIELD = {
    'Denominazione': 'ragione_sociale',
    'Indirizzo': 'indirizzo',
    'Comune': 'citta',
    'CAP': 'cap',
    'Provincia': 'provincia',
    'Note indirizzo': 'note_indirizzo',
    'Paese': 'paese',
    'Indirizzo e-mail': 'email',
    'Referente': 'referente',
    'Telefono': 'telefono',
    'P.IVA/TAX ID': 'piva',
    'Codice Fiscale': 'codice_fiscale',
    'Note': 'note',
    'Indirizzo PEC': 'pec',
    'IBAN': 'iban',
    'Codice SDI': 'codice_sdi',
    'Aliquota iva predefinita': 'aliquota_iva_predefinita',
    'Termini di pagamento': 'termini_pagamento',
    'Indirizzo spedizione': 'indirizzo_spedizione',
    'Sconto predefinito': 'sconto_predefinito',
}


class ImportError_(Exception):
    """Il file non è un export riconoscibile (manca la colonna chiave
    'Denominazione')."""


def parse_rows(file_obj):
    """Legge il file .xlsx (file-like) e restituisce una lista di dict
    {campo_modello: valore}, una per riga con 'Denominazione' non vuota.
    Valori mancanti diventano stringa vuota."""
    workbook = openpyxl.load_workbook(file_obj, data_only=True, read_only=True)
    sheet = workbook.worksheets[0]
    rows_iter = sheet.iter_rows(values_only=True)
    headers = next(rows_iter, None)
    if not headers or 'Denominazione' not in headers:
        raise ImportError_("Il file non ha una colonna 'Denominazione' in prima riga.")

    field_by_col_index = {i: COLUMN_TO_FIELD[h] for i, h in enumerate(headers) if h in COLUMN_TO_FIELD}

    rows = []
    for raw_row in rows_iter:
        record = {}
        for i, value in enumerate(raw_row):
            field = field_by_col_index.get(i)
            if field:
                record[field] = '' if value is None else str(value).strip()
        if record.get('ragione_sociale'):
            rows.append(record)
    return rows
