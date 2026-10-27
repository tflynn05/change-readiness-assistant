---
title: 'Play 10: Automate testing and deployments'
source_id: usds-playbook
source_title: U.S. Digital Services Playbook
author: U.S. Digital Service
license: CC0-1.0 (U.S. public domain)
source_url: https://playbook.cio.gov/#play10
source_path: _plays/10.md
source_commit: f5d71f1939efe87db9f0be414bcfa7c489e01c19
---

Today, developers write automated scripts that can verify thousands of scenarios in minutes and then deploy updated code into production environments multiple times a day. They use automated performance tests which simulate surges in traffic to identify performance bottlenecks. While manual tests and quality assurance are still necessary, automated tests provide consistent and reliable protection against unintentional regressions, and make it possible for developers to confidently release frequent updates to the service.

### Checklist
1. Create automated tests that verify all user-facing functionality
2. Create unit and integration tests to verify modules and components
3. Run tests automatically as part of the build process
4. Perform deployments automatically with deployment scripts, continuous delivery services, or similar techniques
5. Conduct load and performance tests at regular intervals, including before public launch

### Key Questions
- What percentage of the code base is covered by automated tests?
- How long does it take to build, test, and deploy a typical bug fix?
- How long does it take to build, test, and deploy a new feature into production?
- How frequently are builds created?
- What test tools are used?
- Which deployment automation or continuous integration tools are used?
- What is the estimated maximum number of concurrent users who will want to use the system?
- How many simultaneous users could the system handle, according to the most recent capacity test?
- How does the service perform when you exceed the expected target usage volume? Does it degrade gracefully or catastrophically?
- What is your scaling strategy when demand increases suddenly?
