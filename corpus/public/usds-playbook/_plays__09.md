---
title: 'Play 9: Deploy in a flexible hosting environment'
source_id: usds-playbook
source_title: U.S. Digital Services Playbook
author: U.S. Digital Service
license: CC0-1.0 (U.S. public domain)
source_url: https://playbook.cio.gov/#play9
source_path: _plays/09.md
source_commit: f5d71f1939efe87db9f0be414bcfa7c489e01c19
---

Our services should be deployed on flexible infrastructure, where resources can be provisioned in real-time to meet spikes in traffic and user demand. Our digital services are crippled when we host them in data centers that market themselves as “cloud hosting” but require us to manage and maintain hardware directly. This outdated practice wastes time, weakens our disaster recovery plans, and results in significantly higher costs.

### Checklist
1. Resources are provisioned on demand
2. Resources scale based on real-time user demand
3. Resources are provisioned through an API
4. Resources are available in multiple regions
5. We only pay for resources we use
6. Static assets are served through a content delivery network
7. Application is hosted on commodity hardware

### Key Questions
-	Where is your service hosted?
-	What hardware does your service use to run?
-	What is the demand or usage pattern for your service?
-	What happens to your service when it experiences a surge in traffic or load?
-	How much capacity is available in your hosting environment?
-	How long does it take you to provision a new resource, like an application server?
-	How have you designed your service to scale based on demand?
-	How are you paying for your hosting infrastructure (e.g., by the minute, hourly, daily, monthly, fixed)?
-	Is your service hosted in multiple regions, availability zones, or data centers?
-	In the event of a catastrophic disaster to a datacenter, how long will it take to have the service operational?
-	What would be the impact of a prolonged downtime window?
-	What data redundancy do you have built into the system, and what would be the impact of a catastrophic data loss?
-	How often do you need to contact a person from your hosting provider to get resources or to fix an issue?
