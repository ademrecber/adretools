def generate_adre_file(image, layers, style):
    """Gelişmiş 3D ADRE dosyası oluştur"""
    
    style_configs = {
        'modern': {
            'bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'border': '2px solid rgba(255,255,255,0.2)',
            'shadow': '0 20px 40px rgba(0,0,0,0.3)'
        },
        'vintage': {
            'bg': 'linear-gradient(135deg, #8B4513 0%, #D2691E 100%)',
            'border': '3px solid #8B4513',
            'shadow': '0 15px 30px rgba(139,69,19,0.4)'
        },
        'hologram': {
            'bg': 'linear-gradient(135deg, #00f5ff 0%, #ff00ff 50%, #00ff00 100%)',
            'border': '1px solid rgba(255,255,255,0.5)',
            'shadow': '0 25px 50px rgba(0,245,255,0.3)'
        },
        'crystal': {
            'bg': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.3) 100%)',
            'border': '2px solid rgba(255,255,255,0.3)',
            'shadow': '0 30px 60px rgba(255,255,255,0.2)'
        },
        'snow': {
            'bg': 'linear-gradient(135deg, #e6f3ff 0%, #b3d9ff 50%, #80bfff 100%)',
            'border': '3px solid rgba(255,255,255,0.8)',
            'shadow': '0 25px 50px rgba(128,191,255,0.4)'
        },
        'fire': {
            'bg': 'linear-gradient(135deg, #ff4500 0%, #ff6347 30%, #ff8c00 60%, #ffd700 100%)',
            'border': '3px solid rgba(255,69,0,0.8)',
            'shadow': '0 25px 50px rgba(255,69,0,0.6), 0 0 30px rgba(255,140,0,0.4)'
        },

        'rain': {
            'bg': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%)',
            'border': '2px solid rgba(74,144,226,0.6)',
            'shadow': '0 25px 50px rgba(30,60,114,0.6), 0 0 20px rgba(74,144,226,0.3)'
        },
        'lightning': {
            'bg': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 30%, #0f3460 60%, #533483 100%)',
            'border': '2px solid rgba(138,43,226,0.8)',
            'shadow': '0 25px 50px rgba(138,43,226,0.6), 0 0 30px rgba(75,0,130,0.4)'
        },
        'matrix': {
            'bg': 'linear-gradient(135deg, #000000 0%, #001100 50%, #003300 100%)',
            'border': '2px solid rgba(0,255,0,0.6)',
            'shadow': '0 25px 50px rgba(0,0,0,0.8), 0 0 20px rgba(0,255,0,0.3)'
        },
        'galaxy': {
            'bg': 'linear-gradient(135deg, #0c0c0c 0%, #1a0033 30%, #330066 60%, #4d0099 100%)',
            'border': '2px solid rgba(138,43,226,0.6)',
            'shadow': '0 25px 50px rgba(77,0,153,0.6), 0 0 30px rgba(138,43,226,0.4)'
        },

        'neon': {
            'bg': 'linear-gradient(135deg, #ff0080 0%, #ff8000 25%, #80ff00 50%, #0080ff 75%, #8000ff 100%)',
            'border': '2px solid rgba(255,255,255,0.8)',
            'shadow': '0 25px 50px rgba(255,0,128,0.4), 0 0 30px rgba(128,255,0,0.3)'
        },
        'autumn': {
            'bg': 'linear-gradient(135deg, #8B4513 0%, #CD853F 30%, #D2691E 60%, #FF8C00 100%)',
            'border': '2px solid rgba(210,105,30,0.8)',
            'shadow': '0 25px 50px rgba(139,69,19,0.6), 0 0 20px rgba(255,140,0,0.3)'
        },
        'magic': {
            'bg': 'linear-gradient(135deg, #4B0082 0%, #8A2BE2 30%, #9932CC 60%, #FFD700 100%)',
            'border': '2px solid rgba(255,215,0,0.8)',
            'shadow': '0 25px 50px rgba(75,0,130,0.6), 0 0 30px rgba(255,215,0,0.4)'
        }
    }
    
    config = style_configs.get(style, style_configs['modern'])
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>3D Interactive Card - ADRE Format</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: radial-gradient(circle, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
            overflow: hidden;
            font-family: 'Arial', sans-serif;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .card-container {{
            perspective: 800px;
            width: 400px;
            height: 500px;
        }}
        
        .card {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.15s ease-out;
            background: {config['bg']};
            border-radius: 20px;
            border: {config['border']};
            box-shadow: {config['shadow']};
            overflow: hidden;
        }}
        
        .card-face {{
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 18px;
            overflow: hidden;
        }}
        
        .main-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: contrast(1.1) saturate(1.2);
            transform: translateZ(5px);
            border-radius: 18px;
        }}
        
        .shadow-layer {{
            position: absolute;
            top: 5px;
            left: 5px;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.3);
            border-radius: 18px;
            transform: translateZ(-10px);
            pointer-events: none;
            filter: blur(10px);
        }}
        
        .snow-container {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            border-radius: 18px;
        }}
        
        .snowflake {{
            position: absolute;
            top: -10px;
            color: rgba(255,255,255,0.8);
            font-size: 1em;
            animation: snowfall linear infinite;
            pointer-events: none;
        }}
        
        .snowflake:nth-child(1) {{ left: 10%; animation-duration: 3s; animation-delay: 0s; }}
        .snowflake:nth-child(2) {{ left: 20%; animation-duration: 4s; animation-delay: 1s; }}
        .snowflake:nth-child(3) {{ left: 30%; animation-duration: 3.5s; animation-delay: 0.5s; }}
        .snowflake:nth-child(4) {{ left: 40%; animation-duration: 5s; animation-delay: 1.8s; }}
        .snowflake:nth-child(5) {{ left: 50%; animation-duration: 3.2s; animation-delay: 1s; }}
        .snowflake:nth-child(6) {{ left: 60%; animation-duration: 4.5s; animation-delay: 2s; }}
        .snowflake:nth-child(7) {{ left: 70%; animation-duration: 3.8s; animation-delay: 0.2s; }}
        .snowflake:nth-child(8) {{ left: 80%; animation-duration: 4.2s; animation-delay: 1.5s; }}
        
        @keyframes snowfall {{
            0% {{
                transform: translateY(-10px) rotate(0deg);
                opacity: 1;
            }}
            100% {{
                transform: translateY(520px) rotate(360deg);
                opacity: 0;
            }}
        }}
        
        .fire-container {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            border-radius: 18px;
        }}
        
        .flame {{
            position: absolute;
            bottom: -20px;
            color: #ff4500;
            font-size: 2em;
            animation: flicker linear infinite;
            pointer-events: none;
            filter: drop-shadow(0 0 10px #ff6347);
        }}
        
        .flame:nth-child(1) {{ left: 15%; animation-duration: 1.5s; animation-delay: 0s; }}
        .flame:nth-child(2) {{ left: 30%; animation-duration: 1.8s; animation-delay: 0.3s; }}
        .flame:nth-child(3) {{ left: 45%; animation-duration: 1.2s; animation-delay: 0.6s; }}
        .flame:nth-child(4) {{ left: 60%; animation-duration: 1.6s; animation-delay: 0.2s; }}
        .flame:nth-child(5) {{ left: 75%; animation-duration: 1.4s; animation-delay: 0.8s; }}
        .flame:nth-child(6) {{ left: 85%; animation-duration: 1.7s; animation-delay: 0.5s; }}
        
        @keyframes flicker {{
            0% {{
                transform: translateY(0px) scale(1) rotate(-2deg);
                opacity: 0.8;
            }}
            25% {{
                transform: translateY(-30px) scale(1.1) rotate(2deg);
                opacity: 1;
            }}
            50% {{
                transform: translateY(-60px) scale(0.9) rotate(-1deg);
                opacity: 0.9;
            }}
            75% {{
                transform: translateY(-40px) scale(1.05) rotate(1deg);
                opacity: 0.95;
            }}
            100% {{
                transform: translateY(0px) scale(1) rotate(-2deg);
                opacity: 0.8;
            }}
        }}
        
        .rain-drops {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            border-radius: 18px;
        }}
        
        .drop {{
            position: absolute;
            top: -10px;
            width: 2px;
            height: 20px;
            background: linear-gradient(to bottom, rgba(173,216,230,0.8) 0%, rgba(135,206,235,0.6) 50%, transparent 100%);
            border-radius: 50%;
            animation: rainfall linear infinite;
            pointer-events: none;
        }}
        
        .drop:nth-child(1) {{ left: 10%; animation-duration: 0.8s; animation-delay: 0s; }}
        .drop:nth-child(2) {{ left: 20%; animation-duration: 1.2s; animation-delay: 0.2s; }}
        .drop:nth-child(3) {{ left: 30%; animation-duration: 0.9s; animation-delay: 0.4s; }}
        .drop:nth-child(4) {{ left: 40%; animation-duration: 1.1s; animation-delay: 0.1s; }}
        .drop:nth-child(5) {{ left: 50%; animation-duration: 0.7s; animation-delay: 0.6s; }}
        .drop:nth-child(6) {{ left: 60%; animation-duration: 1.3s; animation-delay: 0.3s; }}
        .drop:nth-child(7) {{ left: 70%; animation-duration: 0.8s; animation-delay: 0.5s; }}
        .drop:nth-child(8) {{ left: 80%; animation-duration: 1.0s; animation-delay: 0.7s; }}
        .drop:nth-child(9) {{ left: 15%; animation-duration: 1.1s; animation-delay: 0.8s; }}
        .drop:nth-child(10) {{ left: 85%; animation-duration: 0.9s; animation-delay: 0.9s; }}
        
        @keyframes rainfall {{
            0% {{ transform: translateY(-10px); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(520px); opacity: 0; }}
        }}
        
        /* Lightning Effects */
        .lightning-container {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .lightning-svg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
        .lightning-path {{ animation: lightningStrike 2s infinite; filter: drop-shadow(0 0 8px #fff) drop-shadow(0 0 15px #8A2BE2); stroke-dasharray: 1000; stroke-dashoffset: 1000; }}
        .lightning-path2 {{ animation: lightningStrike 2.5s infinite 0.3s; filter: drop-shadow(0 0 6px #8A2BE2); stroke-dasharray: 800; stroke-dashoffset: 800; }}
        .lightning-path3 {{ animation: lightningStrike 3s infinite 1s; filter: drop-shadow(0 0 6px #4169E1); stroke-dasharray: 900; stroke-dashoffset: 900; }}
        .lightning-path4 {{ animation: lightningStrike 2.2s infinite 1.5s; filter: drop-shadow(0 0 5px #fff); stroke-dasharray: 850; stroke-dashoffset: 850; }}
        .thunder-flash {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.05); animation: thunderFlash 2s infinite; }}
        @keyframes lightningStrike {{ 0%, 85% {{ stroke-dashoffset: 1000; opacity: 0; }} 86% {{ stroke-dashoffset: 0; opacity: 1; }} 88% {{ opacity: 0; }} 89% {{ opacity: 1; }} 90%, 100% {{ opacity: 0; }} }}
        @keyframes thunderFlash {{ 0%, 85%, 100% {{ opacity: 0; }} 86% {{ opacity: 0.3; }} 88% {{ opacity: 0; }} 89% {{ opacity: 0.15; }} }}
        
        /* Matrix Effects */
        .matrix-rain {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; background: rgba(0,0,0,0.3); }}
        .code-stream {{ position: absolute; top: -100px; color: #00ff00; font-family: 'Courier New', monospace; font-size: 10px; writing-mode: vertical-lr; animation: matrixStream linear infinite; text-shadow: 0 0 5px #00ff00; }}
        .code-stream:nth-child(1) {{ left: 5%; animation-duration: 2s; animation-delay: 0s; }}
        .code-stream:nth-child(2) {{ left: 15%; animation-duration: 2.8s; animation-delay: 0.3s; }}
        .code-stream:nth-child(3) {{ left: 25%; animation-duration: 2.2s; animation-delay: 0.6s; }}
        .code-stream:nth-child(4) {{ left: 35%; animation-duration: 3s; animation-delay: 0.9s; }}
        .code-stream:nth-child(5) {{ left: 45%; animation-duration: 2.5s; animation-delay: 0.2s; }}
        .code-stream:nth-child(6) {{ left: 55%; animation-duration: 2.7s; animation-delay: 0.8s; }}
        .code-stream:nth-child(7) {{ left: 65%; animation-duration: 2.3s; animation-delay: 0.5s; }}
        .code-stream:nth-child(8) {{ left: 75%; animation-duration: 2.9s; animation-delay: 1.1s; }}
        .code-stream:nth-child(9) {{ left: 85%; animation-duration: 2.4s; animation-delay: 0.7s; }}
        .code-stream:nth-child(10) {{ left: 95%; animation-duration: 2.6s; animation-delay: 1s; }}
        @keyframes matrixStream {{ 0% {{ transform: translateY(-100px); opacity: 0; }} 10% {{ opacity: 1; }} 90% {{ opacity: 1; }} 100% {{ transform: translateY(600px); opacity: 0; }} }}
        
        /* Galaxy Effects */
        .galaxy-space {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .star {{ position: absolute; width: 2px; height: 2px; background: #fff; border-radius: 50%; animation: twinkle 3s infinite; box-shadow: 0 0 4px #fff; }}
        .star:nth-child(1) {{ top: 15%; left: 20%; animation-delay: 0s; }}
        .star:nth-child(2) {{ top: 35%; left: 75%; animation-delay: 1s; }}
        .star:nth-child(3) {{ top: 65%; left: 25%; animation-delay: 2s; }}
        .star:nth-child(4) {{ top: 85%; left: 80%; animation-delay: 0.5s; }}
        .star:nth-child(5) {{ top: 25%; left: 60%; animation-delay: 1.5s; }}
        .planet {{ position: absolute; width: 20px; height: 20px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #ff6b6b 0%, #4ecdc4 100%); animation: planetOrbit 8s linear infinite; top: 40%; left: 40%; }}
        .planet2 {{ width: 15px; height: 15px; background: radial-gradient(circle at 30% 30%, #feca57 0%, #ff9ff3 100%); animation-duration: 12s; top: 70%; left: 20%; }}
        .comet {{ position: absolute; width: 3px; height: 3px; background: #fff; border-radius: 50%; animation: cometTrail 6s linear infinite; }}
        .comet::after {{ content: ''; position: absolute; width: 30px; height: 2px; background: linear-gradient(to right, #fff 0%, transparent 100%); top: 50%; left: -30px; transform: translateY(-50%); }}
        .comet:nth-child(8) {{ top: 20%; left: -10px; }}
        .comet2 {{ top: 60%; left: -15px; animation-delay: 3s; }}
        .nebula {{ position: absolute; top: 10%; right: 10%; width: 80px; height: 60px; background: radial-gradient(ellipse, rgba(138,43,226,0.3) 0%, rgba(75,0,130,0.2) 50%, transparent 100%); animation: nebulaGlow 4s ease-in-out infinite; border-radius: 50%; }}
        @keyframes twinkle {{ 0%, 100% {{ opacity: 0.3; }} 50% {{ opacity: 1; }} }}
        @keyframes planetOrbit {{ 0% {{ transform: rotate(0deg) translateX(30px) rotate(0deg); }} 100% {{ transform: rotate(360deg) translateX(30px) rotate(-360deg); }} }}
        @keyframes cometTrail {{ 0% {{ transform: translateX(-50px) translateY(0px); opacity: 0; }} 20% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ transform: translateX(450px) translateY(-100px); opacity: 0; }} }}
        @keyframes nebulaGlow {{ 0%, 100% {{ opacity: 0.3; transform: scale(1); }} 50% {{ opacity: 0.6; transform: scale(1.1); }} }}
        
        /* Ocean Effects */
        .ocean-waves {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .wave {{ position: absolute; bottom: 0; width: 100%; height: 30px; background: linear-gradient(to top, rgba(0,179,230,0.3) 0%, transparent 100%); animation: waveMove 3s ease-in-out infinite; }}
        .bubble {{ position: absolute; width: 8px; height: 8px; background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(0,179,230,0.3) 100%); border-radius: 50%; animation: bubbleRise 4s linear infinite; }}
        .bubble:nth-child(2) {{ left: 20%; animation-delay: 0s; }}
        .bubble:nth-child(3) {{ left: 50%; animation-delay: 1s; }}
        .bubble:nth-child(4) {{ left: 70%; animation-delay: 2s; }}
        .bubble:nth-child(5) {{ left: 85%; animation-delay: 3s; }}
        @keyframes waveMove {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} }}
        @keyframes bubbleRise {{ 0% {{ transform: translateY(0px); opacity: 0.8; }} 100% {{ transform: translateY(-400px); opacity: 0; }} }}
        
        /* Neon Effects */
        .neon-lights {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .neon-line {{ position: absolute; width: 2px; height: 100%; background: linear-gradient(to bottom, #ff0080 0%, #80ff00 50%, #0080ff 100%); animation: neonGlow 2s ease-in-out infinite; }}
        .neon-line:nth-child(1) {{ left: 20%; animation-delay: 0s; }}
        .neon-line:nth-child(2) {{ left: 50%; animation-delay: 0.7s; }}
        .neon-line:nth-child(3) {{ left: 80%; animation-delay: 1.4s; }}
        .neon-pulse {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; height: 50px; border: 2px solid #fff; border-radius: 50%; animation: pulse 1.5s ease-in-out infinite; }}
        @keyframes neonGlow {{ 0%, 100% {{ opacity: 0.3; filter: blur(2px); }} 50% {{ opacity: 1; filter: blur(0px); }} }}
        @keyframes pulse {{ 0% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 1; }} 100% {{ transform: translate(-50%, -50%) scale(1.5); opacity: 0; }} }}
        
        /* Autumn Effects */
        .autumn-leaves {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .leaf {{ position: absolute; top: -20px; font-size: 20px; animation: leafFall linear infinite; }}
        .leaf:nth-child(1) {{ left: 10%; animation-duration: 4s; animation-delay: 0s; }}
        .leaf:nth-child(2) {{ left: 30%; animation-duration: 5s; animation-delay: 1s; }}
        .leaf:nth-child(3) {{ left: 60%; animation-duration: 4.5s; animation-delay: 2s; }}
        .leaf:nth-child(4) {{ left: 80%; animation-duration: 3.5s; animation-delay: 0.5s; }}
        .leaf:nth-child(5) {{ left: 45%; animation-duration: 4.2s; animation-delay: 1.5s; }}
        @keyframes leafFall {{ 0% {{ transform: translateY(-20px) rotate(0deg); }} 100% {{ transform: translateY(520px) rotate(360deg); }} }}
        
        /* Magic Effects */
        .magic-realm {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; border-radius: 18px; }}
        .magic-circle {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100px; height: 100px; border: 2px solid #FFD700; border-radius: 50%; animation: magicRotate 8s linear infinite; }}
        .magic-circle::before {{ content: ''; position: absolute; top: -5px; left: -5px; right: -5px; bottom: -5px; border: 1px solid rgba(255,215,0,0.5); border-radius: 50%; animation: magicRotate 6s linear infinite reverse; }}
        .magic-orb {{ position: absolute; width: 12px; height: 12px; background: radial-gradient(circle, #FFD700 0%, #FF6347 100%); border-radius: 50%; animation: orbFloat 4s ease-in-out infinite; box-shadow: 0 0 15px #FFD700; }}
        .magic-orb:nth-child(2) {{ top: 20%; left: 30%; animation-delay: 0s; }}
        .orb2 {{ top: 70%; right: 25%; animation-delay: 2s; background: radial-gradient(circle, #8A2BE2 0%, #4B0082 100%); box-shadow: 0 0 15px #8A2BE2; }}
        .magic-trail {{ position: absolute; width: 2px; height: 40px; background: linear-gradient(to bottom, #FFD700 0%, transparent 100%); animation: trailMove 3s ease-in-out infinite; }}
        .magic-trail:nth-child(4) {{ top: 15%; left: 60%; animation-delay: 0s; }}
        .trail2 {{ top: 60%; left: 15%; animation-delay: 1.5s; background: linear-gradient(to bottom, #8A2BE2 0%, transparent 100%); }}
        .rune {{ position: absolute; width: 20px; height: 20px; border: 2px solid #FFD700; animation: runeGlow 5s ease-in-out infinite; }}
        .rune:nth-child(6) {{ top: 25%; right: 20%; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); animation-delay: 0s; }}
        .rune2 {{ bottom: 25%; left: 20%; clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%); animation-delay: 2.5s; border-color: #8A2BE2; }}
        @keyframes magicRotate {{ 0% {{ transform: translate(-50%, -50%) rotate(0deg); }} 100% {{ transform: translate(-50%, -50%) rotate(360deg); }} }}
        @keyframes orbFloat {{ 0%, 100% {{ transform: translateY(0px) scale(1); }} 50% {{ transform: translateY(-30px) scale(1.3); }} }}
        @keyframes trailMove {{ 0%, 100% {{ opacity: 0; transform: translateY(0px); }} 50% {{ opacity: 1; transform: translateY(-50px); }} }}
        @keyframes runeGlow {{ 0%, 100% {{ opacity: 0.5; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}
        
        .info-overlay {{
            position: absolute;
            bottom: 8px;
            left: 8px;
            background: rgba(0,0,0,0.5);
            padding: 4px 6px;
            border-radius: 4px;
            color: white;
            backdrop-filter: blur(3px);
            text-align: left;
            font-size: 8px;
            max-width: 120px;
        }}
        

        

        
        @media (max-width: 768px) {{
            .card-container {{
                width: 90vw;
                height: 70vh;
                max-width: 350px;
            }}
        }}
    </style>
</head>
<body>

    
    <div class="card-container">
        <div class="card" id="card">
            <div class="card-face">
                <img src="{layers['main']}" alt="Main Image" class="main-image">
                
                <div class="info-overlay">
                    <div>adretools.com</div>
                </div>
            </div>
            
            <!-- 3D Shadow Layer -->
            <div class="shadow-layer"></div>
            
            <!-- Snow Effect -->
            {'<div class="snow-container"><div class="snowflake">❄</div><div class="snowflake">❅</div><div class="snowflake">❆</div><div class="snowflake">❄</div><div class="snowflake">❅</div><div class="snowflake">❆</div><div class="snowflake">❄</div><div class="snowflake">❅</div></div>' if style == 'snow' else ''}
            
            <!-- Fire Effect -->
            {'<div class="fire-container"><div class="flame">🔥</div><div class="flame">🔥</div><div class="flame">🔥</div><div class="flame">🔥</div><div class="flame">🔥</div><div class="flame">🔥</div></div>' if style == 'fire' else ''}
            
            <!-- Smoke Effect -->
            {'<div class="smoke-clouds"><div class="cloud cloud1"></div><div class="cloud cloud2"></div><div class="cloud cloud3"></div><div class="cloud cloud4"></div><div class="cloud cloud5"></div></div>' if style == 'smoke' else ''}
            
            <!-- Rain Effect -->
            {'<div class="rain-drops"><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div><div class="drop"></div></div>' if style == 'rain' else ''}
            
            <!-- Lightning Effect -->
            {'<div class="lightning-container"><svg class="lightning-svg" viewBox="0 0 400 500"><path class="lightning-path" d="M200 0 L180 80 L220 80 L190 150 L230 150 L170 250 L210 250 L160 350 L200 350 L150 450 L190 450 L140 500" stroke="#fff" stroke-width="4" fill="none" opacity="0"/><path class="lightning-path2" d="M180 100 L160 180 L200 180 L170 260 L210 260 L150 360 L190 360 L130 460" stroke="#8A2BE2" stroke-width="2" fill="none" opacity="0"/><path class="lightning-path3" d="M250 0 L230 90 L270 90 L240 170 L280 170 L220 280 L260 280 L200 400 L240 400 L180 500" stroke="#4169E1" stroke-width="3" fill="none" opacity="0"/><path class="lightning-path4" d="M120 0 L140 70 L100 70 L130 140 L90 140 L150 230 L110 230 L170 320 L130 320 L190 420 L150 420 L210 500" stroke="#fff" stroke-width="2" fill="none" opacity="0"/></svg><div class="thunder-flash"></div></div>' if style == 'lightning' else ''}
            
            <!-- Matrix Effect -->
            {'<div class="matrix-rain"><div class="code-stream">01101001</div><div class="code-stream">11000110</div><div class="code-stream">00111010</div><div class="code-stream">10101100</div><div class="code-stream">01010011</div><div class="code-stream">11001010</div><div class="code-stream">00110101</div><div class="code-stream">10011100</div><div class="code-stream">01100011</div><div class="code-stream">11010001</div></div>' if style == 'matrix' else ''}
            
            <!-- Galaxy Effect -->
            {'<div class="galaxy-space"><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="planet"></div><div class="planet planet2"></div><div class="comet"></div><div class="comet comet2"></div><div class="nebula"></div></div>' if style == 'galaxy' else ''}
            
            <!-- Ocean Effect -->
            {'<div class="ocean-waves"><div class="wave"></div><div class="bubble"></div><div class="bubble"></div><div class="bubble"></div><div class="bubble"></div></div>' if style == 'ocean' else ''}
            
            <!-- Neon Effect -->
            {'<div class="neon-lights"><div class="neon-line"></div><div class="neon-line"></div><div class="neon-line"></div><div class="neon-pulse"></div></div>' if style == 'neon' else ''}
            
            <!-- Autumn Effect -->
            {'<div class="autumn-leaves"><div class="leaf">🍂</div><div class="leaf">🍁</div><div class="leaf">🍃</div><div class="leaf">🍂</div><div class="leaf">🍁</div></div>' if style == 'autumn' else ''}
            
            <!-- Magic Effect -->
            {'<div class="magic-realm"><div class="magic-circle"></div><div class="magic-orb"></div><div class="magic-orb orb2"></div><div class="magic-trail"></div><div class="magic-trail trail2"></div><div class="rune"></div><div class="rune rune2"></div></div>' if style == 'magic' else ''}
        </div>
    </div>
    
    <script>
        const card = document.getElementById('card');
        let currentRotationX = 0;
        let currentRotationY = 0;
        
        // Mouse Events - 360° rotation
        let isMouseDown = false;
        let lastMouseX = 0;
        let lastMouseY = 0;
        
        document.addEventListener('mousedown', (e) => {{
            isMouseDown = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }});
        
        document.addEventListener('mouseup', () => {{
            isMouseDown = false;
        }});
        
        document.addEventListener('mousemove', (e) => {{
            if (window.innerWidth > 768) {{
                if (isMouseDown) {{
                    const deltaX = e.clientX - lastMouseX;
                    const deltaY = e.clientY - lastMouseY;
                    
                    currentRotationY += deltaX * 0.5;
                    currentRotationX -= deltaY * 0.5;
                    
                    card.style.transform = `rotateX(${{currentRotationX}}deg) rotateY(${{currentRotationY}}deg) translateZ(50px)`;
                    
                    lastMouseX = e.clientX;
                    lastMouseY = e.clientY;
                }} else {{
                    // Hover effect
                    const rect = card.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    
                    const hoverX = (e.clientX - centerX) / 10;
                    const hoverY = (e.clientY - centerY) / 10;
                    
                    card.style.transform = `rotateX(${{currentRotationX - hoverY}}deg) rotateY(${{currentRotationY + hoverX}}deg) translateZ(50px)`;
                }}
            }}
        }});
        
        // Touch Events for Mobile
        let startX, startY;
        
        card.addEventListener('touchstart', (e) => {{
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }});
        
        card.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            const deltaX = e.touches[0].clientX - startX;
            const deltaY = e.touches[0].clientY - startY;
            
            currentRotationY += deltaX * 0.8;
            currentRotationX -= deltaY * 0.8;
            
            // No limits - allow 360° rotation
            card.style.transform = `rotateX(${{currentRotationX}}deg) rotateY(${{currentRotationY}}deg) translateZ(50px)`;
            
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }});
        
        // Gyroscope for Mobile
        if (window.DeviceOrientationEvent) {{
            window.addEventListener('deviceorientation', (e) => {{
                if (window.innerWidth <= 768) {{
                    const rotateX = e.beta ? e.beta / 1.5 : 0;
                    const rotateY = e.gamma ? e.gamma / 1.5 : 0;
                    
                    card.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translateZ(50px)`;
                }}
            }});
        }}
        
        // Reset on ESC
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0px)';
                currentRotationX = 0;
                currentRotationY = 0;
            }}
        }});
        
        // Mouse leave reset for desktop
        document.addEventListener('mouseleave', () => {{
            if (window.innerWidth > 768) {{
                card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0px)';
            }}
        }});
    </script>
</body>
</html>"""