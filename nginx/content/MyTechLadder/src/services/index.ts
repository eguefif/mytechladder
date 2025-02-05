import instance from './api'
import type { Account } from './types'

export async function postAccount(account: Account) {
  console.log(account)
  let response = await instance.post("create_account/", account)
  console.log(response)
  return response
}

export async function postTest(value: string) {
  return await instance.post("test_post/", { "email": value })
}
