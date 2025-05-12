/**
 * Form Validation Utility
 * 
 * This utility provides functions to validate form inputs.
 */

export type ValidationRule = (value: any) => string | null;
export type ValidationRules = Record<string, ValidationRule[]>;
export type ValidationErrors = Record<string, string | null>;

/**
 * Creates a required field validation rule
 * 
 * @param message - Optional custom error message
 * @returns A validation rule that checks if a field is not empty
 */
export function required(message: string = 'This field is required'): ValidationRule {
  return (value: any) => {
    if (value === null || value === undefined || value === '') {
      return message;
    }
    if (Array.isArray(value) && value.length === 0) {
      return message;
    }
    return null;
  };
}

/**
 * Creates a minimum length validation rule
 * 
 * @param min - The minimum length
 * @param message - Optional custom error message
 * @returns A validation rule that checks if a string has a minimum length
 */
export function minLength(min: number, message?: string): ValidationRule {
  return (value: any) => {
    if (value === null || value === undefined || value === '') {
      return null; // Let required handle empty values
    }
    if (typeof value === 'string' && value.length < min) {
      return message || `Must be at least ${min} characters`;
    }
    return null;
  };
}

/**
 * Creates a maximum length validation rule
 * 
 * @param max - The maximum length
 * @param message - Optional custom error message
 * @returns A validation rule that checks if a string has a maximum length
 */
export function maxLength(max: number, message?: string): ValidationRule {
  return (value: any) => {
    if (value === null || value === undefined || value === '') {
      return null; // Let required handle empty values
    }
    if (typeof value === 'string' && value.length > max) {
      return message || `Must be at most ${max} characters`;
    }
    return null;
  };
}

/**
 * Creates an email validation rule
 * 
 * @param message - Optional custom error message
 * @returns A validation rule that checks if a string is a valid email
 */
export function email(message: string = 'Please enter a valid email address'): ValidationRule {
  return (value: any) => {
    if (value === null || value === undefined || value === '') {
      return null; // Let required handle empty values
    }
    
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (typeof value === 'string' && !emailRegex.test(value)) {
      return message;
    }
    return null;
  };
}

/**
 * Creates a pattern validation rule
 * 
 * @param pattern - The regex pattern to match
 * @param message - Optional custom error message
 * @returns A validation rule that checks if a string matches a pattern
 */
export function pattern(pattern: RegExp, message: string = 'Invalid format'): ValidationRule {
  return (value: any) => {
    if (value === null || value === undefined || value === '') {
      return null; // Let required handle empty values
    }
    if (typeof value === 'string' && !pattern.test(value)) {
      return message;
    }
    return null;
  };
}

/**
 * Validates a form against a set of validation rules
 * 
 * @param values - The form values to validate
 * @param rules - The validation rules to apply
 * @returns An object containing validation errors
 */
export function validateForm(values: Record<string, any>, rules: ValidationRules): ValidationErrors {
  const errors: ValidationErrors = {};
  
  Object.keys(rules).forEach(field => {
    const fieldRules = rules[field];
    const value = values[field];
    
    for (const rule of fieldRules) {
      const error = rule(value);
      if (error) {
        errors[field] = error;
        break;
      }
    }
    
    if (!errors[field]) {
      errors[field] = null;
    }
  });
  
  return errors;
}

/**
 * Checks if a form has any validation errors
 * 
 * @param errors - The validation errors object
 * @returns True if the form has no errors, false otherwise
 */
export function isFormValid(errors: ValidationErrors): boolean {
  return Object.values(errors).every(error => error === null);
}
