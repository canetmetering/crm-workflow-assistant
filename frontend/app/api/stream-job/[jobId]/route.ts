import { NextRequest } from 'next/server'

const RUNNER_URL = 'https://crm-workflow-assistant.onrender.com'

export async function GET(
  request: NextRequest,
  { params }: { params: { jobId: string } }
) {
  const response = await fetch(`${RUNNER_URL}/stream-job/${params.jobId}`, {
    headers: { 'Accept': 'text/event-stream' },
  })

  return new Response(response.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  })
}
