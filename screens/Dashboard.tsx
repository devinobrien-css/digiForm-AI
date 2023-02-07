import { SafeAreaView, Text, View, TouchableOpacity } from 'react-native'
import React from 'react'

const forums = [
  {
    name: "Forum1",
    status: "Pending"
  },
  {
    name: "Forum2",
    status: "Submitted"
  },
  {
    name: "Forum3",
    status: "Pending"
  },
  {
    name: "Forum4",
    status: "Submitted"
  },
  {
    name: "Forum5",
    status: "Pending"
  },
  {
    name: "Forum6",
    status: "Pending"
  },
  {
    name: "Forum7",
    status: "Submitted"
  },
  {
    name: "Forum8",
    status: "Submitted"
  }
]

export default function Dashboard({ switchScreens }: { switchScreens: (status: string) => void }) {
  return (
    <SafeAreaView className='bg-black flex-1'>
      <Text className='text-white text-3xl m-5'>
        Hi there!
      </Text>
      <View className='bg-white m-2 rounded-3xl p-3'>
        <Text className='text-black text-xl mb-5'>Your Current Forums</Text>
        {forums.map((forum: { name: string, status: string }, index) => {
          return (
            <TouchableOpacity key={index} onPress={() => switchScreens(forum.status)}>
              <View className='bg-slate-300 rounded-lg p-2 mb-3 '>
                <View className='flex-row justify-between'>
                  <Text className='text-slate-800 text-sm font-semibold'>Name</Text>
                  <Text className='text-slate-800 text-sm justify-self-start text-center font-semibold'>Status</Text>
                </View>
                <View className='flex-row justify-between items-center'>
                  <Text className='text-slate-800 text-sm'>{forum.name}</Text>
                  <View className={`rounded-lg p-1 ${forum.status === 'Pending' ? 'bg-zinc-100' : 'bg-stone-100'}`}>
                    <Text className='text-slate-800 text-sm'>{forum.status}</Text>
                  </View>
                </View>
              </View>
            </TouchableOpacity>
          )
        })}
      </View>
    </SafeAreaView>
  )
}
