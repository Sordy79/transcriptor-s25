
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página limpia estilo Samsung One UI sin barras adicionales
st.set_page_config(page_title="Modo Intérprete S25", layout="wide", initial_sidebar_state="collapsed")

# Espaciador superior limpio
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Sistema de audio aislado y autoregenerable para evitar cortes
    s25_stable_js = """
    <div style="font-family: system-ui, -apple-system, sans-serif;">
        <button id="mic-btn" style="
            background-color: #2563EB; color: white; font-size: 20px; font-weight: bold;
            padding: 15px; border: none; border-radius: 12px; cursor: pointer; width: 100%; margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        ">🎙️ Iniciar Transcripción en Vivo</button>
        
        <div id="transcript-container" style="
            font-size: 42px; font-weight: 600; line-height: 1.4; color: #FFFFFF; 
            background-color: #1E293B; padding: 25px; border-radius: 16px; 
            min-height: 380px; max-height: 450px; overflow-y: auto; border: 3px solid #3B82F6;
        ">
            <span id="text-area">Presiona el botón para empezar a escuchar...</span>
        </div>
    </div>

    <script>
        const micBtn = document.getElementById('mic-btn');
        const textArea = document.getElementById('text-area');
        const container = document.getElementById('transcript-container');
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            textArea.innerText = "Navegador no compatible. Usa Google Chrome o Microsoft Edge.";
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = true;
            recognition.interimResults = true;
            
            let listening = false;
            let finalText = '';

            micBtn.addEventListener('click', () => {
                if (!listening) { 
                    recognition.start(); 
                } else { 
                    recognition.stop(); 
                }
            });

            recognition.onstart = () => {
                listening = true;
                micBtn.innerText = "🛑 Grabando... Habla de continuo";
                micBtn.style.backgroundColor = "#DC2626";
                textArea.innerHTML = '<span style="color: #93C5FD; font-style: italic;">Escuchando...</span>';
                finalText = '';
            };

            recognition.onend = () => {
                if (listening) {
                    recognition.start();
                } else {
                    micBtn.innerText = "🎙️ Iniciar Transcripción en Vivo";
                    micBtn.style.backgroundColor = "#2563EB";
                }
            };

            recognition.onresult = (event) => {
                let interimText = '';
                let currentFinal = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        currentFinal += event.results[i].transcript + ' ';
                    } else {
                        interimText += event.results[i].transcript;
                    }
                }

                if (currentFinal !== '') {
                    finalText += currentFinal;
                }

                textArea.innerHTML = '<span style="color: #FFFFFF;">' + finalText + '</span>' +
                                     '<span style="color: #93C5FD; font-style: italic;">' + interimText + '</span>';
                
                container.scrollTop = container.scrollHeight;
            };
        }
    </script>
    """
    components.html(s25_stable_js, height=540)

with col2:
    # Campo de respuesta sin título arriba
    user_reply = st.text_area("", placeholder="Escribe aquí tu mensaje para responder...", height=150, label_visibility="collapsed")
    
    if user_reply:
        st.markdown(f"""
            <div style="background-color: #065F46; border: 2px solid #10B981; padding: 15px; border-radius: 12px; margin-top: 15px; margin-bottom: 15px;">
                <p style="color: white; font-size: 28px; font-weight: bold; margin: 0;">{user_reply}</p>
            </div>
        """, unsafe_allow_html=True)
        
    # Botones rápidos sin el título de atajos
    if st.button("👍 Entendido"): st.success("Entendido")
    if st.button("❓ ¿Puedes repetir?"): st.warning("¿Puedes repetir?")
