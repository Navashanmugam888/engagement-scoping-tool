'use client';

import { useRef } from 'react';

export default function useToast() {
  const toastRef = useRef(null);

  const showSuccess = (message, detail = '') => {
    toastRef.current?.show({
      severity: 'success',
      summary: message,
      detail,
      life: 3000,
    });
  };

  const showError = (message, detail = '') => {
    toastRef.current?.show({
      severity: 'error',
      summary: message,
      detail,
      life: 3000,
    });
  };

  const showInfo = (message, detail = '') => {
    toastRef.current?.show({
      severity: 'info',
      summary: message,
      detail,
      life: 3000,
    });
  };

  const showWarn = (message, detail = '') => {
    toastRef.current?.show({
      severity: 'warn',
      summary: message,
      detail,
      life: 3000,
    });
  };

  return {
    toastRef,
    showSuccess,
    showError,
    showInfo,
    showWarn,
  };
}
