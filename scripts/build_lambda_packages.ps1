# Builds deployable Lambda packages by combining each handler's app.py
# with the shared/ utility code into a clean build directory.
# Terraform then zips each build/<handler> folder for deployment.

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$lambdaDir = Join-Path $root "backend\lambda"
$sharedDir = Join-Path $lambdaDir "shared"
$buildDir = Join-Path $root "build"

$handlers = @(
    "list_events_handler",
    "register_handler",
    "get_registrations_handler",
    "cancel_registration_handler"
)

if (Test-Path $buildDir) {
    Remove-Item -Recurse -Force $buildDir
}
New-Item -ItemType Directory -Path $buildDir | Out-Null

foreach ($handler in $handlers) {
    $srcDir = Join-Path $lambdaDir $handler
    $destDir = Join-Path $buildDir $handler

    New-Item -ItemType Directory -Path $destDir | Out-Null

    Copy-Item -Path (Join-Path $srcDir "*.py") -Destination $destDir
    Copy-Item -Path (Join-Path $sharedDir "*.py") -Destination $destDir

    Write-Host "Built package for $handler -> $destDir"
}

Write-Host "All Lambda packages built successfully."