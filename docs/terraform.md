# Terraform Troubleshooting

## Terraform Init Failure

### Problem

`terraform init` fails while initializing a Terraform working directory.

### Common Causes

- Incorrect provider configuration.
- Invalid module source.
- Network connectivity problems.
- Authentication problems.
- Provider or module version constraints.
- Backend configuration issues.

### Troubleshooting

Run:

```bash
terraform init
```

Validate the Terraform configuration:

```bash
terraform validate
```

Check the Terraform version:

```bash
terraform version
```

Review provider and module configuration.

### Resolution

Correct the provider, module, backend, authentication, or network configuration identified in the error.

Run `terraform init` again after correcting the underlying issue.

---

## Terraform Validate Failure

### Problem

`terraform validate` reports configuration errors.

### Common Causes

- Invalid Terraform syntax.
- Incorrect resource arguments.
- Missing required arguments.
- Incorrect resource references.
- Invalid provider configuration.

### Troubleshooting

Run:

```bash
terraform validate
```

Format the configuration:

```bash
terraform fmt -recursive
```

Review the reported file, resource, variable, or configuration block.

### Resolution

Correct the configuration error and run:

```bash
terraform validate
```

again.

---

## Terraform Plan Failure

### Problem

`terraform plan` fails or reports unexpected infrastructure changes.

### Common Causes

- Configuration changes.
- Incorrect variable values.
- Missing resources.
- State differences.
- Provider configuration problems.
- Resource dependency issues.

### Troubleshooting

Run:

```bash
terraform plan
```

Review the resources Terraform wants to create, modify, or destroy.

Check resources tracked in the Terraform state:

```bash
terraform state list
```

Review the Terraform configuration and variables used by the deployment.

### Resolution

Identify whether the planned change is expected.

Do not apply a plan containing unexpected destructive changes until the cause is understood.

---

## Terraform Apply Failure

### Problem

`terraform apply` fails while creating or modifying infrastructure.

### Common Causes

- Cloud authentication failure.
- Insufficient permissions.
- Invalid resource configuration.
- Resource dependency problems.
- Provider errors.
- Existing resources conflicting with the configuration.

### Troubleshooting

Review the error returned by Terraform.

Run:

```bash
terraform plan
```

to understand the intended changes.

Verify cloud credentials and required permissions.

Check the affected resource configuration.

### Resolution

Correct the underlying configuration, permission, dependency, or provider issue before running `terraform apply` again.

---

## Terraform State

### Problem

Terraform state does not match the infrastructure or Terraform cannot find a managed resource.

### Common Causes

- Infrastructure was changed outside Terraform.
- Resources were removed manually.
- Terraform state was changed or restored.
- Terraform configuration no longer matches the state.

### Troubleshooting

List resources tracked by Terraform:

```bash
terraform state list
```

Show details about a resource:

```bash
terraform state show <resource>
```

Inspect the current state:

```bash
terraform show
```

### Resolution

Compare the Terraform configuration, state, and actual infrastructure.

Do not manually edit the Terraform state file unless there is a clear reason and the impact is understood.

---

## Terraform State Lock

### Problem

Terraform reports that the state is locked and cannot be modified.

### Common Causes

- Another Terraform operation is currently running.
- A previous Terraform operation failed while holding the lock.
- A CI/CD pipeline stopped unexpectedly.

### Troubleshooting

Check whether another Terraform process or CI/CD pipeline is currently running.

Review the backend configuration and lock information.

### Resolution

If another Terraform operation is active, wait for it to complete.

If the lock is stale and it is confirmed that no Terraform operation is running, follow the backend-specific procedure to safely remove the lock.

Do not force-unlock an active Terraform operation.

---

## Terraform Resource Drift

### Problem

The actual infrastructure differs from the configuration managed by Terraform.

### Common Causes

- Manual changes were made in the cloud environment.
- Another automation system changed the resource.
- Terraform configuration was changed without applying it.

### Troubleshooting

Run:

```bash
terraform plan
```

Review the differences between the Terraform configuration, state, and actual infrastructure.

### Resolution

Determine whether the external change should be retained.

If the infrastructure change should be managed by Terraform, update the configuration or import the resource when appropriate.

If the Terraform configuration should remain the source of truth, apply the intended configuration only after reviewing the plan.

---

## Terraform Import

### Problem

An existing infrastructure resource needs to be managed by Terraform.

### Troubleshooting

Identify the existing resource and determine the correct Terraform resource type and resource ID.

Import the resource:

```bash
terraform import <resource_address> <resource_id>
```

Review the resulting state:

```bash
terraform state show <resource_address>
```

Run:

```bash
terraform plan
```

### Resolution

Update the Terraform configuration so that it accurately represents the imported resource.

The goal is for the configuration and state to match the existing infrastructure without unexpected changes.

---

## Terraform Variables

### Problem

Terraform reports missing or incorrect variable values.

### Common Causes

- A required variable is not provided.
- An incorrect variable value is supplied.
- A variable has the wrong type.
- The wrong variable file is being used.

### Troubleshooting

Review variable definitions and the Terraform configuration.

Use a variable file when appropriate:

```bash
terraform plan -var-file="terraform.tfvars"
```

Check the values being supplied to the Terraform configuration.

### Resolution

Provide the required variables with the correct values and types.

Avoid storing sensitive values directly in Terraform configuration files.

---

## Terraform Provider Issues

### Problem

Terraform cannot initialize or use a provider correctly.

### Common Causes

- Incorrect provider version.
- Provider authentication failure.
- Provider configuration is missing.
- Network connectivity problems.

### Troubleshooting

Check the provider configuration and required versions.

Run:

```bash
terraform init
```

Review the Terraform configuration for the provider.

Check provider dependencies:

```bash
terraform providers
```

### Resolution

Correct the provider configuration, version constraint, or authentication configuration and run Terraform initialization again.

---

## Terraform Dependency Issues

### Problem

Terraform cannot create or update resources because required resource dependencies are incorrect or unavailable.

### Common Causes

- Incorrect resource references.
- Missing dependencies.
- Incorrect resource configuration.
- Resources are being created in an unexpected order.

### Troubleshooting

Review resource references in the Terraform configuration.

Check the Terraform dependency graph:

```bash
terraform graph
```

Run:

```bash
terraform plan
```

Review the planned resource dependencies and changes.

### Resolution

Correct resource references or dependency configuration.

Use explicit dependencies only when Terraform cannot determine the dependency automatically.

---

## Terraform Destroy Safety

### Problem

Terraform plans to destroy infrastructure that may still be required.

### Troubleshooting

Run:

```bash
terraform plan
```

Carefully review resources marked for destruction.

Identify why Terraform believes the resource should be removed.

Review recent configuration changes and state differences.

### Resolution

Do not run `terraform apply` until unexpected destructive changes are understood.

If the resource is still required, correct the Terraform configuration or state relationship before applying changes.

---

## Terraform Troubleshooting Workflow

When troubleshooting a Terraform issue:

1. Read the Terraform error message carefully.
2. Identify whether the problem is related to configuration, provider, state, authentication, dependency, or infrastructure.
3. Run `terraform fmt` and `terraform validate`.
4. Run `terraform plan` to understand the intended changes.
5. Check Terraform state when resources are missing or inconsistent.
6. Verify cloud credentials and required permissions.
7. Investigate unexpected resource changes before applying them.
8. Never apply unexpected destructive changes without understanding the cause.
9. Apply the smallest safe change.
10. Verify the infrastructure after a successful deployment.