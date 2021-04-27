package com.example.mylib

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

class Notification (val context: Context) {
    fun createNotificationChannel(
            channelId: String,
            name: String,
            description: String,
            importance: Int = NotificationManager.IMPORTANCE_DEFAULT,
            showBadge: Boolean = false) {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId,name,importance)
            channel.setShowBadge(showBadge)
            channel.description = description
            val notificationManager = context.getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun <T: AppCompatActivity>getPendingIntent(
//            cls: Class<AppCompatActivity>,
            cls: Class<T>,
            requestCode:Int,
            flag: Int = PendingIntent.FLAG_UPDATE_CURRENT):PendingIntent{

        val intent = Intent(context,cls)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        val pendingIntent = PendingIntent.getActivity(context,requestCode,intent,flag)

        return pendingIntent
    }

    fun <T: AppCompatActivity> getPendingIntent(
        cls: Class<T>,
        requestCode: Int,
        message: String,
        flag: Int = PendingIntent.FLAG_UPDATE_CURRENT): PendingIntent {
        val intent = Intent(context, cls)
        intent.putExtra("message", message)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                Intent.FLAG_ACTIVITY_CLEAR_TASK
        val pendingIntent = PendingIntent.getActivity(context, requestCode, intent, flag)

        return pendingIntent
    }


    fun notifyBasic(channelId:String,notification_id:Int,
                    title : String,content : String, icon: Int, bitmap : Bitmap,
                    pendingIntent: PendingIntent){
//        val builder = NotificationCompat.Builder(context,channelId)
//        builder.setSmallIcon(icon)
//        builder.setContentTitle(title)
//        builder.setContentText(content)
//        builder.priority = NotificationCompat.PRIORITY_DEFAULT
//        builder.setAutoCancel(true)
//        builder.setContentIntent(pendingIntent)
//
//        val notificationManager = NotificationManagerCompat.from(context)
//        notificationManager.notify(notification_id,builder.build())

        NotificationCompat.Builder(context,channelId).apply {
            setSmallIcon(icon)
            setContentTitle(title)
            setContentText(content)
            setLargeIcon(bitmap)
            priority = NotificationCompat.PRIORITY_DEFAULT
            setAutoCancel(true)
            setContentIntent(pendingIntent)
            NotificationManagerCompat
                    .from(context)
                    .notify(notification_id,build())
        }
    }
}