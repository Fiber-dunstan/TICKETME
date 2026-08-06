# Deploys the frontend to S3 and invalidates the CloudFront cache so
# changes go live immediately instead of waiting for cache expiry.
#
# Usage: .\scripts\deploy_frontend.ps1

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$frontendDir = Join-Path $root "frontend"
$infraDir = Join-Path $root "infrastructure"

Write-Host "Reading deployment targets from Terraform outputs..."
Push-Location $infraDir
$bucketName = terraform output -raw frontend_bucket_name
$frontendUrl = terraform output -raw frontend_url
$distributionId = terraform output -raw cloudfront_distribution_id
Pop-Location

Write-Host "Target bucket: $bucketName"
Write-Host "Syncing frontend files to S3..."

aws s3 sync $frontendDir "s3://$bucketName" --delete

Write-Host "Creating CloudFront invalidation (clears cached files)..."
aws cloudfront create-invalidation --distribution-id $distributionId --paths "/*"

Write-Host ""
Write-Host "Deployment complete!"
Write-Host "Your site is live at: $frontendUrl"
Write-Host "(Note: it may take 1-2 minutes for the CloudFront invalidation to fully propagate.)"