# PyPI Publishing Configuration
# ============================

## Repository Configuration
This package is configured to publish ONLY to the official PyPI repository:
- **Official PyPI**: https://pypi.org/project/whatsapp-api-py/
- **Repository URL**: https://upload.pypi.org/legacy/

## NOT Published To:
- ❌ TestPyPI (test.pypi.org)
- ❌ Any other package repositories
- ❌ Private repositories

## Publishing Method:
- ✅ GitHub Actions with Trusted Publishing
- ✅ Automatic on GitHub releases
- ✅ Official PyPI API endpoints only

## Environment:
- **Environment Name**: `pypi`
- **Repository**: Official PyPI only
- **Authentication**: OIDC Trusted Publishing (no API tokens needed)

## Workflow Files:
- `.github/workflows/publish.yml` - Simple release publishing
- `.github/workflows/ci-cd.yml` - Full CI/CD with testing

Both workflows explicitly specify the official PyPI repository URL to ensure
no accidental publishing to test repositories.
