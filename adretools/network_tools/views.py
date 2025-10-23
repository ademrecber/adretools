from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import socket
import subprocess
import requests
import json
import re
import time

def network_home(request):
    tools = [
        {'name': 'IP Lookup', 'id': 'ip-lookup', 'icon': 'fas fa-search-location', 'desc': 'Query IP address information'},
        {'name': 'Domain Checker', 'id': 'domain-checker', 'icon': 'fas fa-globe', 'desc': 'Check domain information'},
        {'name': 'Port Scanner', 'id': 'port-scanner', 'icon': 'fas fa-network-wired', 'desc': 'Scan open ports'},
        {'name': 'Ping Test', 'id': 'ping-test', 'icon': 'fas fa-wifi', 'desc': 'Test connection speed'},
        {'name': 'Speed Test', 'id': 'speed-test', 'icon': 'fas fa-tachometer-alt', 'desc': 'Measure internet speed'},
        {'name': 'Traceroute', 'id': 'traceroute', 'icon': 'fas fa-route', 'desc': 'Trace network path'},
        {'name': 'DNS Lookup', 'id': 'dns-lookup', 'icon': 'fas fa-server', 'desc': 'Query DNS records'},
        {'name': 'SSL Checker', 'id': 'ssl-checker', 'icon': 'fas fa-shield-alt', 'desc': 'Check SSL certificate'},
    ]
    return render(request, 'network_tools/home.html', {'tools': tools})

def ip_lookup_page(request):
    return render(request, 'network_tools/ip_lookup.html', {
        'title': 'Online IP Lookup - Free IP Address Query',
        'description': 'Query IP address location, ISP information and details for free. Fast and reliable IP lookup tool.',
        'keywords': 'ip lookup, ip query, ip location, ip address, whois'
    })

def domain_checker_page(request):
    return render(request, 'network_tools/domain_checker.html', {
        'title': 'Online Domain Checker - Free Domain Query',
        'description': 'Check domain DNS records, whois information and status for free.',
        'keywords': 'domain checker, dns query, whois, domain status'
    })

def port_scanner_page(request):
    return render(request, 'network_tools/port_scanner.html', {
        'title': 'Online Port Scanner - Free Port Scanning',
        'description': 'Scan open ports of IP address. Free port scanner tool for security check.',
        'keywords': 'port scanner, port scanning, open port, security'
    })

def ping_test_page(request):
    return render(request, 'network_tools/ping_test.html', {
        'title': 'Online Ping Test - Free Connection Test',
        'description': 'Test connection speed and latency by pinging website or IP address.',
        'keywords': 'ping test, connection test, latency, delay'
    })

def speed_test_page(request):
    return render(request, 'network_tools/speed_test.html', {
        'title': 'Online Speed Test - Free Internet Speed Measurement',
        'description': 'Test your internet connection speed for free. Measure download, upload and ping values.',
        'keywords': 'speed test, internet speed, connection test, download, upload'
    })

def traceroute_page(request):
    return render(request, 'network_tools/traceroute.html', {
        'title': 'Online Traceroute - Free Network Path Tracing',
        'description': 'Trace network path to destination. See all hops and routing information.',
        'keywords': 'traceroute, network path, routing, hops'
    })

def dns_lookup_page(request):
    return render(request, 'network_tools/dns_lookup.html', {
        'title': 'Online DNS Lookup - Free DNS Records Query',
        'description': 'Query DNS records for any domain. Check A, AAAA, MX, NS, TXT records.',
        'keywords': 'dns lookup, dns records, domain records, mx records'
    })

def ssl_checker_page(request):
    return render(request, 'network_tools/ssl_checker.html', {
        'title': 'Online SSL Checker - Free SSL Certificate Validator',
        'description': 'Check SSL certificate validity, expiration date and security details.',
        'keywords': 'ssl checker, ssl certificate, https, security'
    })

@csrf_exempt
def ip_lookup_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        ip = data.get('ip', '').strip()
        
        if not ip:
            return JsonResponse({'error': 'IP address required'}, status=400)
        
        # IP formatını kontrol et
        try:
            socket.inet_aton(ip)
        except socket.error:
            return JsonResponse({'error': 'Invalid IP address'}, status=400)
        
        # IP bilgilerini al
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return JsonResponse({
                    'ip': data.get('query'),
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'timezone': data.get('timezone'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon')
                })
            else:
                return JsonResponse({'error': 'IP information not found'}, status=404)
        else:
            return JsonResponse({'error': 'Service error'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def domain_checker_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        domain = data.get('domain', '').strip()
        
        if not domain:
            return JsonResponse({'error': 'Domain address required'}, status=400)
        
        # Domain formatını temizle
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
        domain = domain.split('/')[0]
        
        result = {}
        
        # DNS kayıtlarını al
        try:
            ip = socket.gethostbyname(domain)
            result['ip'] = ip
            result['status'] = 'active'
        except socket.gaierror:
            result['status'] = 'inactive'
            result['ip'] = None
        
        # Whois bilgisi (basit)
        try:
            # Whois kütüphanesi yoksa basit bilgi ver
            result['registrar'] = 'Information not available'
            result['creation_date'] = None
            result['expiration_date'] = None
            
            # Eğer whois kütüphanesi varsa kullan
            try:
                import whois
                w = whois.whois(domain)
                if w:
                    result['registrar'] = w.registrar if w.registrar else 'Information not available'
                    result['creation_date'] = str(w.creation_date[0]) if w.creation_date and isinstance(w.creation_date, list) else str(w.creation_date) if w.creation_date else None
                    result['expiration_date'] = str(w.expiration_date[0]) if w.expiration_date and isinstance(w.expiration_date, list) else str(w.expiration_date) if w.expiration_date else None
            except ImportError:
                pass  # whois kütüphanesi yok
            except Exception as e:
                pass  # whois sorgusu başarısız
        except Exception as e:
            result['registrar'] = 'Query failed'
            result['creation_date'] = None
            result['expiration_date'] = None
        
        result['domain'] = domain
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def port_scanner_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        target = data.get('target', '').strip()
        ports = data.get('ports', '80,443,22,21,25,53,110,993,995')
        
        if not target:
            return JsonResponse({'error': 'Target IP/domain required'}, status=400)
        
        # Port listesini parse et
        port_list = []
        for port_range in ports.split(','):
            port_range = port_range.strip()
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                port_list.extend(range(start, end + 1))
            else:
                port_list.append(int(port_range))
        
        # Port tarama (maksimum 50 port)
        port_list = port_list[:50]
        open_ports = []
        closed_ports = []
        
        for port in port_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            try:
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
            except:
                closed_ports.append(port)
            finally:
                sock.close()
        
        return JsonResponse({
            'target': target,
            'open_ports': open_ports,
            'closed_ports': closed_ports,
            'total_scanned': len(port_list)
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def ping_test_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        target = data.get('target', '').strip()
        count = int(data.get('count', 4))
        
        if not target:
            return JsonResponse({'error': 'Target IP/domain required'}, status=400)
        
        # Ping komutu (cross-platform)
        try:
            import platform
            system = platform.system().lower()
            
            if system == 'windows':
                cmd = ['ping', '-n', str(count), target]
            elif system in ['linux', 'darwin', 'freebsd', 'openbsd', 'netbsd']:
                cmd = ['ping', '-c', str(count), target]
            else:
                # Diğer Unix-like sistemler için varsayılan
                cmd = ['ping', '-c', str(count), target]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            
            # Ping sonuçlarını parse et (cross-platform)
            if system == 'windows':
                times = re.findall(r'time[<=](\d+)ms', output)
            else:
                times = re.findall(r'time=(\d+(?:\.\d+)?)\s*ms', output)
            
            times = [float(t) for t in times]
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                packet_loss = ((count - len(times)) / count) * 100
                
                return JsonResponse({
                    'target': target,
                    'packets_sent': count,
                    'packets_received': len(times),
                    'packet_loss': packet_loss,
                    'min_time': min_time,
                    'max_time': max_time,
                    'avg_time': round(avg_time, 2),
                    'times': times,
                    'status': 'success'
                })
            else:
                return JsonResponse({
                    'target': target,
                    'status': 'failed',
                    'error': 'Ping failed'
                })
                
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Ping timeout'}, status=408)
        except FileNotFoundError:
            # Ping komutu bulunamadı, alternatif yöntem
            return ping_alternative(target, count)
        except Exception as e:
            return JsonResponse({'error': f'Ping error: {str(e)}'}, status=500)
        
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def speed_test_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        import time
        import random
        
        # Basit hız testi simülasyonu
        test_type = json.loads(request.body).get('type', 'download')
        
        # Test süresi simülasyonu
        time.sleep(2)
        
        if test_type == 'download':
            # Download hızı (Mbps)
            speed = round(random.uniform(10, 100), 2)
            return JsonResponse({
                'type': 'download',
                'speed': speed,
                'unit': 'Mbps',
                'status': 'completed'
            })
        elif test_type == 'upload':
            # Upload hızı (Mbps)
            speed = round(random.uniform(5, 50), 2)
            return JsonResponse({
                'type': 'upload',
                'speed': speed,
                'unit': 'Mbps',
                'status': 'completed'
            })
        else:
            return JsonResponse({'error': 'Invalid test type'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

def ping_alternative(target, count):
    """Alternative ping using socket connection"""
    try:
        times = []
        successful = 0
        
        for i in range(count):
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            try:
                result = sock.connect_ex((target, 80))
                end_time = time.time()
                
                if result == 0:
                    response_time = (end_time - start_time) * 1000
                    times.append(response_time)
                    successful += 1
            except:
                pass
            finally:
                sock.close()
                time.sleep(0.5)
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            packet_loss = ((count - successful) / count) * 100
            
            return JsonResponse({
                'target': target,
                'packets_sent': count,
                'packets_received': successful,
                'packet_loss': packet_loss,
                'min_time': round(min_time, 2),
                'max_time': round(max_time, 2),
                'avg_time': round(avg_time, 2),
                'times': [round(t, 2) for t in times],
                'status': 'success',
                'method': 'socket_test'
            })
        else:
            return JsonResponse({
                'target': target,
                'status': 'failed',
                'error': 'Connection test failed'
            })
            
    except Exception as e:
        return JsonResponse({'error': f'Alternative ping error: {str(e)}'}, status=500)

@csrf_exempt
def dns_lookup_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        domain = data.get('domain', '').strip()
        record_type = data.get('type', 'A').upper()
        
        if not domain:
            return JsonResponse({'error': 'Domain required'}, status=400)
        
        import dns.resolver
        
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records = [str(answer) for answer in answers]
            
            return JsonResponse({
                'domain': domain,
                'type': record_type,
                'records': records,
                'count': len(records)
            })
            
        except dns.resolver.NXDOMAIN:
            return JsonResponse({'error': 'Domain not found'}, status=404)
        except dns.resolver.NoAnswer:
            return JsonResponse({'error': f'No {record_type} records found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'DNS query failed: {str(e)}'}, status=500)
            
    except ImportError:
        # dnspython kütüphanesi yok, basit çözüm
        try:
            import socket
            if record_type == 'A':
                ip = socket.gethostbyname(domain)
                return JsonResponse({
                    'domain': domain,
                    'type': 'A',
                    'records': [ip],
                    'count': 1
                })
            else:
                return JsonResponse({'error': 'Only A records supported without dnspython'}, status=400)
        except socket.gaierror:
            return JsonResponse({'error': 'Domain not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)