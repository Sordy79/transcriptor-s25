
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página estilo Samsung One UI
st.set_page_config(page_title="Modo Intérprete S25", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #3B82F6; text-align: center; margin-bottom: 20px; }
    .section-label { font-size: 20px; font-weight: bold; color: #9CA3AF; margin-bottom: 5px; }
    iframe { border: none !important; }
    </style>
    <p class="main-title">📱 Transcriptor en Tiempo Real (Estilo Galaxy S25)</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns()

with col1:
    st.markdown('<p class="section-label">🧏 Transcripción Instantánea (Voz a Texto):</p>', unsafe_allow_html=True)
    
    # Motor JavaScript optimizado para transcripción fluida (Stream de texto)
    s25_realtime_js = """
    <div style="font-family: system-ui, -apple-system, sans-serif;">
        <button id="mic-btn" style="
            background-color: #2563EB; color: white; font-size: 20px; font-weight: bold;
            padding: 15px; border: none; border-radius: 12px; cursor: pointer; width: 100%; margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        ">🎙️ Iniciar Transcripción en Vivo</button>
        
        <div id="transcript-container" style="
            font-size: 42px; font-weight: 600; line-height: 1.4; color: #FFFFFF; 
            background-color: #1E293B; padding: 25px; border-radius: 16px; 
            min-height: 350px; max-height: 450px; overflow-y: auto; border: 3px solid #3B82F6;
        ">
            <span id="final-text" style="color: #FFFFFF;"></span>
            <span id="interim-text" style="color: #93C5FD; font-style: italic;">Presiona el botón para empezar a escuchar...</span>
        </div>
    </div>

    <script>
        const micBtn = document.getElementById('mic-btn');
        const finalTextSpan = document.getElementById('final-text');
        const interimTextSpan = document.getElementById('interim-text');
        const container = document.getElementById('transcript-container');
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            interimTextSpan.innerText = "Navegador no compatible. Por favor, usa Google Chrome o Microsoft Edge.";
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = true;
            
            // ESTA ES LA CLAVE: Activa resultados provisionales en tiempo real
            recognition.interimResults = true; 
            
            let listening = false;
            let completeTranscript = '';

            micBtn.addEventListener('click', () => {
                if (!listening) { 
                    recognition.start(); 
                } else { 
                    recognition.stop(); 
                }
            });

            recognition.onstart = () => {
                listening = true;
                micBtn.innerText = "🛑 Grabando... Habla ahora";
                micBtn.style.backgroundColor = "#DC2626";
                interimTextSpan.innerText = " Escuchando...";
                finalTextSpan.innerText = "";
                completeTranscript = "";
            };

            recognition.onend = () => {
                listening = false;
                micBtn.innerText = "🎙️ Iniciar Transcripción en Vivo";
                micBtn.style.backgroundColor = "#2563EB";
                if(finalTextSpan.innerText === "" && completeTranscript === "") {
                    interimTextSpan.innerText = "Presiona el botón para empezar a escuchar...";
                } else {
                    interimTextSpan.innerText = "";
                }
            };

            recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }

                // Guardamos el texto ya procesado e imprimimos el que se está hablando al segundo
                completeTranscript += finalTranscript;
                finalTextSpan.innerText = completeTranscript;
                interimTextSpan.innerText = interimTranscript;
                
                // Auto-scroll hacia abajo automático para leer siempre lo último
                container.scrollTop = container.scrollHeight;
            };
        }
    </script>
    """
    components.html(s25_realtime_js, height=540)

with col2:
    st.markdown('<p class="section-label">⌨️ Escribe una respuesta rápida:</p>', unsafe_allow_html=True)
    user_reply = st.text_area("La otra persona leerá esto en grande:", placeholder="Escribe aquí tu mensaje...", height=120)
    
    if user_reply:
        st.markdown(f"""
            <div style="background-color: #065F46; border: 2px solid #10B981; padding: 15px; border-radius: 12px;">
                <p style="color: white; font-size: 28px; font-weight: bold; margin: 0;">{user_reply}</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<p class="section-label" style="margin-top:20px;">⚡ Atajos de teclado visuales:</p>', unsafe_allow_html=True)
    if st.button("👍 Entendido"): st.success("Entendido")
    if st.button("❓ ¿Puedes repetir?"): st.warning("¿Puedes repetir?")
