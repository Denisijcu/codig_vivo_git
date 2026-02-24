package com.example.codigovivoexampleapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.codigovivoexampleapp.ui.theme.CodigoVivoExampleAppTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST
import java.util.concurrent.TimeUnit
// -----------------------------
// MODELO DE DATOS Y API
// -----------------------------
data class HiveRequest(val tarea: String)
data class HiveResponse(val status: String, val resultado: String)

interface VertexApiService {
    @Headers("ngrok-skip-browser-warning: true") // IMPORTANTE: Esto permite que la App pase directo al API
    @POST("/ejecutar")
    suspend fun dispararColmena(@Body request: HiveRequest): HiveResponse
}

// -----------------------------
// UI STATE
// -----------------------------
data class VertexUiState(
    val isProcessing: Boolean = false,
    val resultado: String = ""
)

// -----------------------------
// VIEWMODEL (Conexión Real)
// -----------------------------
class VertexViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(VertexUiState())
    val uiState: StateFlow<VertexUiState> = _uiState.asStateFlow()


    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(2, TimeUnit.MINUTES) // Tiempo para conectar
        .readTimeout(5, TimeUnit.MINUTES)    // Tiempo para esperar la respuesta de la Colmena
        .writeTimeout(2, TimeUnit.MINUTES)
        .build()

    // Configuración de Retrofit
    // RECUERDA: Pon tu IP local (Flask) aquí.
    private val api = Retrofit.Builder()
        .baseUrl("https://ee33-2601-589-4100-b642-fed3-f4d0-1cca-50c8.ngrok-free.app")
        .client(okHttpClient) // <--- Agregamos el cliente con paciencia
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(VertexApiService::class.java)

    fun dispararColmena(tarea: String) {
        if (tarea.isBlank()) return

        viewModelScope.launch {
            _uiState.value = VertexUiState(isProcessing = true, resultado = "Iniciando Colmena...")

            try {
                val response = api.dispararColmena(HiveRequest(tarea))
                _uiState.value = VertexUiState(
                    isProcessing = false,
                    resultado = response.resultado
                )
            } catch (e: Exception) {
                _uiState.value = VertexUiState(
                    isProcessing = false,
                    resultado = "ERROR DE CONEXIÓN:\n${e.localizedMessage}\n\nVerifica que Flask esté corriendo y la IP sea correcta."
                )
            }
        }
    }
}

// -----------------------------
// SCREEN (Jetpack Compose)
// -----------------------------
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VertexCommandScreen(
    modifier: Modifier = Modifier,
    viewModel: VertexViewModel
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    var tareaInput by remember { mutableStateOf("") }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFF1A1A1A))
            .padding(16.dp)
    ) {

        Text(
            text = "🚀 VERTEX HIVE COMMAND",
            color = Color.Green,
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = tareaInput,
            onValueChange = { tareaInput = it },
            label = { Text("Tarea para la Colmena", color = Color.Gray) },
            modifier = Modifier.fillMaxWidth(),
            textStyle = LocalTextStyle.current.copy(color = Color.White),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Color.Green,
                unfocusedBorderColor = Color.Gray,
                cursorColor = Color.Green,
                focusedLabelColor = Color.Green
            )
        )

        Button(
            onClick = { viewModel.dispararColmena(tareaInput) },
            modifier = Modifier
                .padding(top = 16.dp)
                .fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = Color.Green),
            enabled = !state.isProcessing
        ) {
            Text("DISPARAR COLMENA", color = Color.Black)
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (state.isProcessing) {
            LinearProgressIndicator(
                modifier = Modifier.fillMaxWidth(),
                color = Color.Yellow,
                trackColor = Color.DarkGray
            )
            Text(
                text = "⚙️ Los Sombreros están debatiendo...",
                color = Color.Yellow,
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(top = 4.dp)
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            "RESULTADO DEL CTO:",
            color = Color.Gray,
            style = MaterialTheme.typography.labelLarge
        )

        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .background(Color.Black)
                .border(1.dp, Color.DarkGray)
                .padding(8.dp)
        ) {
            SelectionContainer {
                Text(
                    text = if (state.resultado.isEmpty())
                        "Esperando órdenes..."
                    else state.resultado,
                    color = Color(0xFF00FF00),
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.verticalScroll(rememberScrollState())
                )
            }
        }
    }
}

// -----------------------------
// MAIN ACTIVITY
// -----------------------------
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            CodigoVivoExampleAppTheme {
                val vertexViewModel: VertexViewModel = viewModel()

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    containerColor = Color(0xFF1A1A1A)
                ) { innerPadding ->
                    VertexCommandScreen(
                        modifier = Modifier.padding(innerPadding),
                        viewModel = vertexViewModel
                    )
                }
            }
        }
    }
}