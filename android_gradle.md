  // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0") // Para parsear el JSON de la Colmena
    implementation("com.squareup.okhttp3:logging-interceptor:4.11.0") // Para ver los logs en el Logcat

    // Lifecycle & Coroutines
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.6.1")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.6.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1")

    // Jetpack Compose (Versiones base)
    implementation("androidx.activity:activity-compose:1.7.2")
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material:material:1.5.0") // Para el LinearProgressIndicator
    implementation("androidx.compose.ui:ui-tooling-preview:1.5.0")
