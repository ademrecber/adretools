from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import re
import base64
import html
import urllib.parse
import datetime
import time
import sqlparse

def dev_home(request):
    tools = [
        {'name': 'JSON Formatter', 'id': 'json-formatter', 'icon': 'fab fa-js-square', 'desc': 'Validate, format and minify JSON'},
        {'name': 'Hash Generator', 'id': 'hash-generator', 'icon': 'fas fa-fingerprint', 'desc': 'Generate MD5, SHA1, SHA256 hashes'},
        {'name': 'Regex Tester', 'id': 'regex-tester', 'icon': 'fas fa-search', 'desc': 'Test regular expressions'},
        {'name': 'Base64 Encoder', 'id': 'base64-encoder', 'icon': 'fas fa-lock', 'desc': 'Base64 encode/decode'},
        {'name': 'URL Encoder', 'id': 'url-encoder', 'icon': 'fas fa-link', 'desc': 'URL encode/decode'},
        {'name': 'HTML Encoder', 'id': 'html-encoder', 'icon': 'fab fa-html5', 'desc': 'HTML encode/decode'},
        {'name': 'SQL Formatter', 'id': 'sql-formatter', 'icon': 'fas fa-database', 'desc': 'Format SQL queries'},
        {'name': 'Timestamp Converter', 'id': 'timestamp-converter', 'icon': 'fas fa-clock', 'desc': 'Convert Unix timestamps'},
        {'name': 'XML Formatter', 'id': 'xml-formatter', 'icon': 'fas fa-code', 'desc': 'Format and visualize XML'},
        {'name': 'E-Invoice Viewer', 'id': 'invoice-viewer', 'icon': 'fas fa-file-invoice', 'desc': 'View XML invoices as formatted documents'},
    ]
    return render(request, 'dev_tools/home.html', {'tools': tools})

def json_formatter_page(request):
    return render(request, 'dev_tools/json_formatter.html', {
        'title': 'Online JSON Formatter - Free JSON Validator',
        'description': 'Validate, format and minify your JSON data. Free online JSON formatter tool.',
        'keywords': 'json formatter, json validator, json minify, json beautify'
    })

def hash_generator_page(request):
    return render(request, 'dev_tools/hash_generator.html', {
        'title': 'Online Hash Generator - MD5 SHA1 SHA256 Free',
        'description': 'Generate MD5, SHA1, SHA256 hash values for your text. Secure and free hash generator.',
        'keywords': 'hash generator, md5, sha1, sha256, hash calculator'
    })

def regex_tester_page(request):
    return render(request, 'dev_tools/regex_tester.html', {
        'title': 'Online Regex Tester - Regular Expression Test Tool',
        'description': 'Test your regular expression (regex) patterns. Live results and explanations.',
        'keywords': 'regex tester, regular expression, pattern matching, regex test'
    })

@csrf_exempt
def json_formatter_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        json_text = data.get('json_text', '').strip()
        action = data.get('action', 'format')
        
        if not json_text:
            return JsonResponse({'error': 'JSON text required'}, status=400)
        
        # JSON'u parse et
        try:
            parsed_json = json.loads(json_text)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        
        if action == 'format':
            # Güzel formatla
            formatted = json.dumps(parsed_json, indent=2, ensure_ascii=False)
            return JsonResponse({'result': formatted, 'valid': True})
        elif action == 'minify':
            # Minify et
            minified = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=False)
            return JsonResponse({'result': minified, 'valid': True})
        else:
            return JsonResponse({'error': 'Invalid operation'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def hash_generator_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({'error': 'Text required'}, status=400)
        
        # Hash'leri oluştur
        text_bytes = text.encode('utf-8')
        
        hashes = {
            'md5': hashlib.md5(text_bytes).hexdigest(),
            'sha1': hashlib.sha1(text_bytes).hexdigest(),
            'sha256': hashlib.sha256(text_bytes).hexdigest(),
            'sha512': hashlib.sha512(text_bytes).hexdigest()
        }
        
        return JsonResponse({'hashes': hashes})
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def regex_tester_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        pattern = data.get('pattern', '').strip()
        text = data.get('text', '').strip()
        flags = data.get('flags', '')
        
        if not pattern:
            return JsonResponse({'error': 'Regex pattern required'}, status=400)
        
        # Flags'i parse et
        regex_flags = 0
        if 'i' in flags:
            regex_flags |= re.IGNORECASE
        if 'm' in flags:
            regex_flags |= re.MULTILINE
        if 's' in flags:
            regex_flags |= re.DOTALL
        
        try:
            # Regex'i compile et
            compiled_regex = re.compile(pattern, regex_flags)
            
            # Eşleşmeleri bul
            matches = []
            for match in compiled_regex.finditer(text):
                matches.append({
                    'match': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'groups': match.groups()
                })
            
            return JsonResponse({
                'matches': matches,
                'match_count': len(matches),
                'valid': True
            })
            
        except re.error as e:
            return JsonResponse({'error': f'Invalid regex: {str(e)}'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

def base64_encoder_page(request):
    return render(request, 'dev_tools/base64_encoder.html', {
        'title': 'Online Base64 Encoder/Decoder - Free',
        'description': 'Encode and decode Base64 strings online for free',
        'keywords': 'base64 encoder, base64 decoder, base64 converter'
    })

def url_encoder_page(request):
    return render(request, 'dev_tools/url_encoder.html', {
        'title': 'Online URL Encoder/Decoder - Free',
        'description': 'Encode and decode URLs online for free',
        'keywords': 'url encoder, url decoder, url converter'
    })

def html_encoder_page(request):
    return render(request, 'dev_tools/html_encoder.html', {
        'title': 'Online HTML Encoder/Decoder - Free',
        'description': 'Encode and decode HTML entities online for free',
        'keywords': 'html encoder, html decoder, html entities'
    })

def sql_formatter_page(request):
    return render(request, 'dev_tools/sql_formatter.html', {
        'title': 'Online SQL Formatter - Free',
        'description': 'Format and beautify SQL queries online for free',
        'keywords': 'sql formatter, sql beautifier, sql format'
    })

def timestamp_converter_page(request):
    return render(request, 'dev_tools/timestamp_converter.html', {
        'title': 'Online Timestamp Converter - Free',
        'description': 'Convert Unix timestamps to human readable dates',
        'keywords': 'timestamp converter, unix timestamp, date converter'
    })

def xml_formatter_page(request):
    return render(request, 'dev_tools/xml_formatter.html', {
        'title': 'Online XML Formatter - Free XML Validator',
        'description': 'Format, validate and visualize XML data with syntax highlighting',
        'keywords': 'xml formatter, xml validator, xml viewer, xml beautifier'
    })

def invoice_viewer_page(request):
    return render(request, 'dev_tools/invoice_viewer.html', {
        'title': 'E-Invoice XML Viewer - Free',
        'description': 'View your XML e-invoices in a formatted document view',
        'keywords': 'e-invoice, xml invoice, invoice viewer, xml viewer'
    })

@csrf_exempt
def base64_encoder_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        action = data.get('action', 'encode')
        
        if not text:
            return JsonResponse({'error': 'Text required'}, status=400)
        
        if action == 'encode':
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return JsonResponse({'result': encoded})
        elif action == 'decode':
            try:
                decoded = base64.b64decode(text).decode('utf-8')
                return JsonResponse({'result': decoded})
            except Exception:
                return JsonResponse({'error': 'Invalid Base64 string'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def url_encoder_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        action = data.get('action', 'encode')
        
        if not text:
            return JsonResponse({'error': 'Text required'}, status=400)
        
        if action == 'encode':
            encoded = urllib.parse.quote(text)
            return JsonResponse({'result': encoded})
        elif action == 'decode':
            try:
                decoded = urllib.parse.unquote(text)
                return JsonResponse({'result': decoded})
            except Exception:
                return JsonResponse({'error': 'Invalid URL encoding'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def html_encoder_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        action = data.get('action', 'encode')
        
        if not text:
            return JsonResponse({'error': 'Text required'}, status=400)
        
        if action == 'encode':
            encoded = html.escape(text)
            return JsonResponse({'result': encoded})
        elif action == 'decode':
            try:
                decoded = html.unescape(text)
                return JsonResponse({'result': decoded})
            except Exception:
                return JsonResponse({'error': 'Invalid HTML encoding'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def sql_formatter_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        sql_text = data.get('sql_text', '').strip()
        action = data.get('action', 'format')
        
        if not sql_text:
            return JsonResponse({'error': 'SQL text required'}, status=400)
        
        if action == 'format':
            formatted = sqlparse.format(sql_text, reindent=True, keyword_case='upper')
            return JsonResponse({'result': formatted})
        elif action == 'minify':
            minified = sqlparse.format(sql_text, strip_comments=True, strip_whitespace=True)
            return JsonResponse({'result': minified})
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def timestamp_converter_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        action = data.get('action', 'to_date')
        
        if action == 'to_date':
            timestamp = data.get('timestamp', '')
            if not timestamp:
                return JsonResponse({'error': 'Timestamp required'}, status=400)
            
            try:
                ts = int(timestamp)
                dt = datetime.datetime.fromtimestamp(ts)
                return JsonResponse({
                    'date': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'iso': dt.isoformat(),
                    'utc': datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
                })
            except (ValueError, OSError):
                return JsonResponse({'error': 'Invalid timestamp'}, status=400)
        
        elif action == 'to_timestamp':
            date_str = data.get('date', '')
            if not date_str:
                return JsonResponse({'error': 'Date required'}, status=400)
            
            try:
                dt = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp())
                return JsonResponse({'timestamp': timestamp})
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)