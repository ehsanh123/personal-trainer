import { useState, useEffect } from 'react'
import { MESSAGES } from '../utils'

const submitMsgInitiaState = { isErrorMessage: false, msg: '' }

export const useMsgAfterSubmit = (lastResult: string) => {
  const [submitMsg, setSubmitMsg] = useState(submitMsgInitiaState)
  const setMsg = (submitMessage: string, isErrorMessage = false) => {
    setSubmitMsg({ msg: submitMessage, isErrorMessage })
    setTimeout(() => setSubmitMsg(submitMsgInitiaState), 1500)
  }

  useEffect(() => {
    if (lastResult === "correct") {
      setMsg(MESSAGES.ANSWER_SUBMIT.SUCCESS)
    } else if (lastResult === "wrong") {
      setMsg(MESSAGES.ANSWER_SUBMIT.ERROR, true)
    } else if (lastResult === "waveClear") {
      setMsg("Wave Cleared!", false)
    }
  }, [lastResult])

  return submitMsg
}
