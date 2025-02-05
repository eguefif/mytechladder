import instance from './api'
import type { Account } from './types'

export async function postAccount(account: Account) {
  console.log(account)
  let response = await instance.post("create_account/", account)
  return response
}
