const pollStatus = (realTaskId: string) => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  setConnectionStatus('Connected')

  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${apiUrl}/scan/${realTaskId}`, {
        headers: { 'ngrok-skip-browser-warning': 'true' }
      })
      if (!res.ok) return
      const data = await res.json()
      setLatestProgress(data.progress ?? 0)
      setLatestStep(data.step ?? '')
      setMessages(prev => [...prev, data])
      if (data.progress === 100) {
        setResults(data.results)
        setIsScanning(false)
        setConnectionStatus('Completed')
        clearInterval(interval)
      }
      if (data.error || data.status === 'failed') {
        setConnectionStatus('Failed')
        setIsScanning(false)
        clearInterval(interval)
      }
    } catch (err) {
      console.error('Poll error:', err)
    }
  }, 3000)
}