import { SafeAreaView, Text, View, TouchableOpacity } from 'react-native'
import React, { useEffect, useState } from 'react'
import axios from 'axios'


export default function Dashboard({ switchScreens }: { switchScreens: (status: string) => void }) {
  const [forums, setForums] : any = useState({})
  useEffect(()=>{
    axios.get('http://192.168.1.223:8000/getAllForms/',{
      data: undefined
    },).then(res => {
      setForums(res.data)
    }).catch((err)=>console.log(err))
  },[])
  return (
    <SafeAreaView className=' flex-1'>
      <Text className='text-black text-3xl m-5'>
        Hi there!
      </Text>
      <View className='bg-black m-2 rounded-3xl p-5 h-[600]'>
        <Text className='text-white text-xl my-5'>Your Current Forums</Text>
        {
        Object.keys(forums).length > 0 ? 
         Object.keys(forums).map((key: any, index) => {
          return (
            <TouchableOpacity key={index} onPress={() => switchScreens(forums[key].complete ? '': 'Form')}>
              <View className='bg-slate-300 rounded-lg p-3 py-5 mb-3 '>
                <View className='flex-row justify-between items-center mb-3'>
                  <Text className='text-slate-800 text-lg'>{forums[key].name}</Text>
                  <Text className='text-slate-800 text-lg'>{forums[key].due}</Text>
                </View>
                <View className='flex-row justify-between items-center'>
                  <Text className='text-slate-800 text-sm'>{forums[key].organizer}</Text>
                  <View className={`rounded-lg p-1 ${forums[key].complete ? 'bg-zinc-100' : 'bg-stone-100'}`}>
                    <Text className='text-slate-800 text-sm'>{forums[key].complete ? 'Submitted': 'Pending'}</Text>
                  </View>
                </View>
              </View>
            </TouchableOpacity>
          )
        }):<Text>No Items</Text>}
      </View>
    </SafeAreaView>
  )
}
