# PowerShell script to run "python -m streamlit" with passed arguments
# Construct the command
$command = "python -m streamlit"

# Append all arguments to the command
foreach ($arg in $args) {
    $command += " $arg"
}

# Execute the command
Invoke-Expression $command