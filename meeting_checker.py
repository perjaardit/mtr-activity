import subprocess


def get_meeting_info_from_event_logs():
    powershell_script = r'''
    $ErrorActionPreference = 'Stop'
    $meetingEvents = Get-WinEvent -
        LogName = 'Microsoft-Windows-Teams/Operational'

    $meetingInfo = @()

    foreach ($event in $meetingEvents) {
        $properties = $event.Properties

        $startTime = $properties[0].Value
        $endTime = $properties[1].Value
        $subject = $properties[2].Value
        $organizer = $properties[3].Value

        $meetingInfo += @{
            'Start Time' = $startTime
            'End Time' = $endTime
            'Subject' = $subject
            'Organizer' = $organizer
        }
    }

    $meetingInfo | ConvertTo-Json
    '''

    command = [
        'powershell.exe',
        '-Command',
        '-'
    ]

    # Execute the PowerShell script to retrieve meeting information from the event logs
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)
    output, error = process.communicate(input=powershell_script.encode('utf-8'))

    if process.returncode == 0:
        return output.decode('utf-8')
    else:
        print(f"Error executing PowerShell script: {error.decode('utf-8').strip()}")
        return None


# Example usage
meeting_info = get_meeting_info_from_event_logs()
print(meeting_info)
