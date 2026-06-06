'use client'

import { useState } from 'react'

export default function Home() {
  const [repoUrl, setRepoUrl] = useState('https://github.com/juice-shop/juice-shop')
  const [taskId, setTaskId] = useState('')
  const [messages, setMessages] = useState<any[]>([])
  const [connectionStatus, setConnectionStatus] = useState('Disconnected')
  const [latestProgress, setLatestProgress] = useState(0)
  const [latestStep, setLatestStep] = useState('')
  const [results, setResults] = useState<any>(null)
  const [isScanning, setIsScanning] = useState(false)

  const pollStatus = (realTaskId: string) => {
    const apiUrl = const apiUrl = '/api'
    setConnectionStatus('Connected')

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${apiUrl}/scan/${realTaskId}`, {
          headers: { 'ngrok-skip-browser-warning': 'true' }
        })

        if (!res.ok) return

        const data = await res.json()
        console.log('Poll result:', data)

        setLatestProgress(data.progress ?? 0)
        setLatestStep(data.step ?? '')
        setMessages(prev => [...prev, data])

        if (data.progress === 100) {
          setResults(data.results)
          setIsScanning(false)
          setConnectionStatus('Completed')
          clearInterval(interval)
        }

        if (data.error) {
          setConnectionStatus('Error: ' + data.error)
          setIsScanning(false)
          clearInterval(interval)
        }

        if (data.status === 'failed') {
          setConnectionStatus('Failed')
          setIsScanning(false)
          clearInterval(interval)
        }

      } catch (err) {
        console.error('Poll error:', err)
      }
    }, 3000)
  }

  const startScan = async () => {
    if (!repoUrl.trim()) {
      alert('Please enter a repository URL')
      return
    }

    setMessages([])
    setResults(null)
    setLatestProgress(0)
    setLatestStep('')
    setTaskId('')
    setIsScanning(true)
    setConnectionStatus('Starting...')

    try {
      const apiUrl = const apiUrl = '/api'

      const response = await fetch(
        `${apiUrl}/scan?repo_url=${encodeURIComponent(repoUrl.trim())}`,
        {
          method: 'POST',
          headers: { 'ngrok-skip-browser-warning': 'true' }
        }
      )

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`Server error ${response.status}: ${text}`)
      }

      const data = await response.json()
      console.log('Scan started:', data)

      if (data.status === 'cached') {
        setConnectionStatus('Completed (Cached)')
        setLatestProgress(100)
        setLatestStep('Cached result — no changes since last scan')
        setResults({
          results: [],
          message: data.message,
          total_findings: data.total_findings
        })
        setIsScanning(false)
        return
      }

      const realTaskId: string = data.task_id
      setTaskId(realTaskId)
      pollStatus(realTaskId)

    } catch (err: any) {
      console.error('Failed to start scan:', err)
      setConnectionStatus('Failed: ' + err.message)
      setIsScanning(false)
    }
  }

  const totalFindings = results?.results?.length ?? results?.total_findings ?? 0

  return (
    <main className="min-h-screen bg-gray-950 text-gray-100 p-10 font-mono">
      <h1 className="text-3xl font-bold mb-2 text-white">AI Security Auditor</h1>
      <p className="text-gray-400 mb-8 text-sm">Semgrep-powered vulnerability scanner</p>

      <div className="mb-4">
        <input
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="https://github.com/owner/repo"
          disabled={isScanning}
          className="w-full bg-gray-900 border border-gray-700 text-white p-3 rounded text-sm focus:outline-none focus:border-gray-400 disabled:opacity-50"
        />
      </div>

      <button
        onClick={startScan}
        disabled={isScanning}
        className="bg-white text-black px-6 py-2 rounded text-sm font-bold hover:bg-gray-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
      >
        {isScanning ? 'Scanning...' : 'Start Scan'}
      </button>

      <div className="mt-6 text-sm text-gray-400">
        Status: <span className={`font-bold ${
          connectionStatus === 'Connected' ||
          connectionStatus === 'Completed' ||
          connectionStatus === 'Completed (Cached)'
            ? 'text-green-400'
            : connectionStatus.startsWith('Error') ||
              connectionStatus.startsWith('Failed')
            ? 'text-red-400'
            : 'text-yellow-400'
        }`}>{connectionStatus}</span>
      </div>

      {taskId && (
        <div className="mt-1 text-xs text-gray-600">
          Task ID: <code className="text-gray-400">{taskId}</code>
        </div>
      )}

      {(isScanning || latestProgress > 0) && (
        <div className="mt-6">
          <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>{latestStep || 'Waiting...'}</span>
            <span>{latestProgress}%</span>
          </div>
          <div className="w-full bg-gray-800 rounded h-2">
            <div
              className="bg-green-400 h-2 rounded transition-all duration-700"
              style={{ width: `${latestProgress}%` }}
            />
          </div>
        </div>
      )}

      {results && (
        <div className="mt-8 border border-green-800 rounded p-5 bg-green-950">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-green-400 text-lg">✅</span>
            <h2 className="font-bold text-green-300">Scan Complete</h2>
          </div>
          <p className="text-sm text-gray-300 mb-3">
            Total findings: <strong className="text-white">{totalFindings}</strong>
          </p>
          {results.message && (
            <p className="text-xs text-yellow-400 mb-3">{results.message}</p>
          )}
          {results.errors?.length > 0 && (
            <div className="mb-3 p-3 bg-red-950 border border-red-800 rounded text-xs text-red-300">
              <strong>Errors:</strong>
              {results.errors.map((e: any, i: number) => (
                <div key={i}>{e.message}</div>
              ))}
            </div>
          )}
          <pre className="text-xs overflow-auto bg-gray-900 p-3 rounded border border-gray-700 max-h-72 text-gray-300">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}

      {messages.length > 0 && (
        <div className="mt-8">
          <h2 className="text-sm font-bold text-gray-400 mb-3">LOG</h2>
          <div className="space-y-2">
            {messages.map((msg, index) => (
              <div key={index} className="border border-gray-800 p-3 rounded text-xs bg-gray-900">
                <span className="text-green-400">{msg.progress}%</span>
                <span className="text-gray-500 mx-2">—</span>
                <span className="text-gray-300">{msg.step}</span>
                {msg.error && (
                  <span className="text-red-400 ml-2">⚠ {msg.error}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  )
}