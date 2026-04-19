# VPC — Virtual Private Cloud

## What is a VPC?

Your private network inside AWS. Like having your own data center inside AWS's cloud.

```
AWS Cloud
└── VPC (your private network: 10.0.0.0/16)
    ├── Public Subnet  (10.0.1.0/24) → has route to Internet Gateway
    │   └── EC2 (web server, load balancer)
    └── Private Subnet (10.0.2.0/24) → no direct internet access
        └── EC2 (app server, RDS database)
```

---

## Core Components

| Component | What it does |
| --- | --- |
| **VPC** | Your isolated virtual network, you define the IP range (CIDR) |
| **Subnet** | Subdivision of VPC. Public = internet reachable, Private = internal only |
| **Internet Gateway (IGW)** | Door between your VPC and the public internet |
| **NAT Gateway** | Lets private subnet instances reach internet (outbound only) |
| **Route Table** | Rules for where traffic goes. Each subnet has one. |
| **Security Group** | Firewall at instance level. Stateful (return traffic auto-allowed) |
| **NACL** | Firewall at subnet level. Stateless (must allow both directions) |

---

## CIDR Notation

```
10.0.0.0/16  →  65,536 IPs  (16 bits fixed, 16 bits free)
10.0.1.0/24  →  256 IPs     (24 bits fixed, 8 bits free)
10.0.1.0/28  →  16 IPs      (28 bits fixed, 4 bits free)

AWS reserves 5 IPs per subnet (first 4 + last 1)
So /24 gives you 256 - 5 = 251 usable IPs
```

---

## Public vs Private Subnet

```
Public Subnet:
  Route table has:  0.0.0.0/0 → Internet Gateway
  Instance needs:   public IP or Elastic IP
  Use for:          Load balancers, Bastion hosts, NAT Gateway

Private Subnet:
  Route table has:  0.0.0.0/0 → NAT Gateway (for outbound only)
  No public IP
  Use for:          App servers, databases, caches
```

---

## Security Group vs NACL

```
Security Group (SG):
  - Attached to EC2 instances
  - Stateful: if you allow inbound, response is auto-allowed outbound
  - Allow rules only (no explicit deny)
  - Evaluated as a whole (all rules checked)

NACL (Network ACL):
  - Attached to subnets
  - Stateless: must explicitly allow both inbound AND outbound
  - Allow AND deny rules
  - Rules evaluated in order (lowest number first)
```

---

## Common Architecture Pattern

```
Internet → Route 53 → ALB (public subnet)
                         ↓
               EC2 App Servers (private subnet)
                         ↓
               RDS PostgreSQL (private subnet, different AZ)
                         ↓ (outbound only, e.g. npm install)
               NAT Gateway → Internet Gateway → Internet
```

---

## Key Interview Points

- VPC is **regional**, subnets are **AZ-specific**
- Default VPC exists in every region with public subnets
- VPC Peering: connect two VPCs (no overlapping CIDR)
- VPC Endpoints: access S3/DynamoDB without internet (stays within AWS network)
- Flow Logs: capture IP traffic for debugging/security audit
