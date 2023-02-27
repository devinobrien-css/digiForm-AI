import { Button, SafeAreaView, ScrollView, Text, TextInput, TouchableOpacity, View } from 'react-native'
import CheckBox from 'expo-checkbox';
import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function Fill_Form() {
    const [form, setForm]: any = useState({})
    const [details, setDetails]: any = useState({})
    useEffect(() => {
        axios.get('http://192.168.1.223:8000/getForm/0', {
            data: undefined
        },).then(res => {
            console.log(res.data.data)
            setForm(res.data.fields)
            setDetails(res.data.data)
        }).catch((err) => console.log(err))
    }, [])
    const handleTextChange = (key: any, val: any) => {
        setForm({
            ...form, [key]: {
                ...form[key],
                value: val
            }
        })
    }

    const handleCheckboxChange = (key: any) => {
        setForm({
            ...form, [key]: {
                ...form[key],
                value: form[key].value === 'Yes' ? 'No' : 'Yes'
            }
        })
    }

    const handleMCSingleValue = (key: any) => {
        let form_copy = {
            ...form, [key]: {
                ...form[key],
                value: form[key].value === 'Yes' ? 'No' : 'Yes'
            }
        }

        if (form[key].value === 'No')
            Object.keys(form).map((k) => {
                if (form[k].groupName === form[key].groupName && k !== key) {
                    console.log(form[k].name)
                    form_copy = {
                        ...form_copy, [k]: {
                            ...form_copy[k],
                            value: 'No'
                        }
                    }
                }
            })
        setForm(form_copy)
    }
    console.log(form)
    return (
        <SafeAreaView>
            <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
                <View className='flex-1 flex-column items-center'>
                    <Text className='text-2xl font-bold my-2'>{details?.name}</Text>
                    <Text className='text-md font-semibold'>{details?.organizer}</Text>
                </View>
                <View className='flex-1 mx-10 my-5'>
                    {Object.keys(form).length > 0 ?
                        Object.keys(form).map((key: any, index) => {
                            return (
                                <View key={index}>
                                    {
                                        form[key].type === 'text' ?
                                            <>
                                                <Text className='text-bold'>{form[key].name}</Text>
                                                <TextInput value={form[key].value} onChangeText={text => handleTextChange(key, text)} className='border-2 rounded-xl mt-2 mb-5 p-5' />
                                            </>
                                            : form[key].type === 'checkbox' ?
                                                <View className='flex flex-row mb-5'>
                                                    <Text className='mr-5'>{form[key].name}</Text>
                                                    <CheckBox value={form[key].value === 'Yes' ? true : false} onValueChange={() => handleCheckboxChange(key)} />
                                                </View>
                                                : form[key].type === "mc" && form[key].singleSelectionOnly
                                                    ? <View className='mb-5'>
                                                        {form[key - 1].groupName !== form[key].groupName && <Text className='mb-2'>{form[key].groupName}</Text>}
                                                        <View className='flex flex-row mb-1'><CheckBox value={form[key].value === 'Yes' ? true : false} onValueChange={() => handleMCSingleValue(key)} /><Text className='ml-5'>{form[key].choiceName}</Text></View>
                                                    </View>
                                                    : form[key].type === "mc" && !form[key].singleSelectionOnly
                                                        ? <View className='mb-5'>
                                                            {form[key - 1].groupName !== form[key].groupName && <Text className='mb-2'>{form[key].groupName}</Text>}
                                                            <View className='flex flex-row mb-1'><CheckBox value={form[key].value === 'Yes' ? true : false} onValueChange={() => handleCheckboxChange(key)} /><Text className='ml-5'>{form[key].choiceName}</Text></View>
                                                        </View>
                                                        : <></>

                                    }
                                </View>
                            )
                        }) :
                        <Text>No Items</Text>
                    }
                </View>
                <View className='flex-1 flex-row justify-center'>
                    <TouchableOpacity className='border-2 rounded-xl bg-black py-3 px-5'>
                        <Text className='text-white'>Submit</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </SafeAreaView>
    )
}

