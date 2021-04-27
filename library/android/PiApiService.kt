package com.example.mylib.openapi.piapi

import com.example.mylib.openapi.piapi.data.WeatherCast
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query


interface PiApiService {
    @GET("/api/led")
    fun controlLed(
            @Query("target") target: String,
            @Query("value") value: String
    ):Call<WeatherCast>

    @GET("/api/servo")
    fun controlServo(
            @Query("target") target:String,
            @Query("value") value:Int
    ): Call<WeatherCast>

    @GET("/api/buzzer")
    fun controlBuzzer(
            @Query("target") target: String,
            @Query("value") value: String
    ):Call<WeatherCast>

}

object PiApi : OpenApi(){
    override val TAG = javaClass.simpleName
    override val BASE_URL = "http://172.30.1.13:8000"

    private val service = retrofit.create(PiApiService::class.java)

    fun controlLed(target: String,value: String,callback:(WeatherCast)->Unit){
    service.controlLed(target,value)
            .enqueue(ApiCallback<WeatherCast>(callback))
    }

    fun controlServo(target: String,value: Int,callback:(WeatherCast)->Unit){
        service.controlServo(target,value)
                .enqueue(ApiCallback<WeatherCast>(callback))
    }

    fun controlBuzzer(target: String,value: String,callback:(WeatherCast)->Unit){
        service.controlBuzzer(target,value)
                .enqueue(ApiCallback<WeatherCast>(callback))
    }
}

//object PiApi{
//    val TAG = javaClass.simpleName
//    private val retrofit = Retrofit.Builder()
//            .baseUrl("http://192.168.0.34:8000")
//            .addConverterFactory(GsonConverterFactory.create())
//            .build()
//
//    fun getService() = retrofit.create(PiApiService::class.java)
//
//    fun controlLed(target: String, value: String, callback: (ControlResult)->Unit){
//        getService()
//                .controlLed(target,value)
//                .enqueue(object : Callback<ControlResult> {
//                    override fun onFailure(call: Call<ControlResult>, t: Throwable) {
//                        Log.e(TAG,t.toString())
//                    }
//
//                    override fun onResponse(call: Call<ControlResult>, response: Response<ControlResult>) {
//                        if(response.isSuccessful){
//                            val result = response.body()
//                            callback(result!!)
//                        }else {
//                            Log.w(TAG,"${response.code()}, ${response.message()}")
//                            Log.w(OpenWeather.TAG,"${response.toString()}")
//                        }
//                    }
//                })
//    }
//
//    fun controlServo(target: String,value: Int,callback: (ControlResult) -> Unit){
//        getService()
//                .controlServo(target,value)
//                .enqueue(object : Callback<ControlResult>{
//                    override fun onFailure(call: Call<ControlResult>, t: Throwable) {
//                        Log.e(TAG,t.toString())
//                    }
//
//                    override fun onResponse(call: Call<ControlResult>, response: Response<ControlResult>) {
//                        if(response.isSuccessful){
//                            val result = response.body()
//                            callback(result!!)
//                        }else {
//                            Log.w(TAG,"${response.code()}, ${response.message()}")
//                            Log.w(OpenWeather.TAG,"${response.toString()}")
//                        }
//                    }
//                })
//    }
//}