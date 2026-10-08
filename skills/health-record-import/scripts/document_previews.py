"""Optional local previews for private review; original bytes remain immutable."""
import base64
import hashlib
import io
from pathlib import Path


def attach_previews(model, archive_root, config):
    root = Path(archive_root).resolve()
    requested = {did for q in model.get('review_questions', []) for did in q.get('document_ids', [])}
    requested.update(r.get('source_document_id') for rows in model.get('tables', {}).values()
                     for r in rows if r.get('review_status') in ('needs_review', 'unreadable'))
    requested.update(r.get('source_document_id') for r in model.get('pending_corrections', []))
    requested.update(d['entry_id'] for d in model['documents'] if d.get('missing_pages'))
    requested.discard(None)
    edge = int(config.get('original_preview_max_edge', 2000))
    if not 500 <= edge <= 3000:
        raise ValueError('Preview size outside limits')
    count = 0
    for d in model['documents']:
        if d['entry_id'] not in requested or not d.get('original_path'):
            continue
        original = (root / d['original_path']).resolve()
        if root not in original.parents:
            raise ValueError('Original path escapes private archive')
        if not original.is_file():
            d['preview_note'] = 'Original unavailable at the saved path'
            continue
        raw = original.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        expected = d.get('received_sha256')
        if not expected:
            raise ValueError('Original checksum required before embedding')
        if digest != expected:
            raise ValueError('Original checksum changed')
        mime = d.get('mime_type') or ''
        if mime in ('image/jpeg', 'image/png', 'image/webp', 'image/gif'):
            from PIL import Image, ImageOps
            with Image.open(io.BytesIO(raw)) as source:
                image = ImageOps.exif_transpose(source).convert('RGB')
                image.thumbnail((edge, edge))
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=92, optimize=True)
            d['original_preview'] = {'kind': 'image', 'data_url': 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii'),
                                     'source_sha256': digest, 'width': image.width, 'height': image.height,
                                     'note': 'Reduced preview; open the linked original for full detail.'}
            count += 1
        elif mime.startswith('text/') and len(raw) <= 256000:
            d['original_preview'] = {'kind': 'text', 'text': raw.decode('utf-8-sig'), 'source_sha256': digest,
                                     'note': 'Saved source text; this is not a scan.'}
            count += 1
        else:
            d['preview_note'] = 'Open the original link; an inline preview was not generated for this format.'
        if hashlib.sha256(original.read_bytes()).hexdigest() != digest:
            raise ValueError('Original changed during rendering')
    model['original_preview_counts'] = {'documents_with_embedded_preview': count, 'requested_source_documents': len(requested), 'network_used': False}
    return model
