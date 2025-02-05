import instance from './api'
import type { Account } from './types'

export async function postAccount(account: Account) {
  console.log(account)
  let response = await instance.post("create_account/", account)
  return response
}

export async function postTest(value: string) {
  await instance.post("test_post/", { "email": value })
}
