import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  failed: boolean;
}

// Catches a render failure in the view below it and shows a way back instead
// of an empty page. Any navigation clears the failure, so the next route
// renders normally without a reload.
export class ErrorBoundary extends Component<Props, State> {
  state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.warn('View failed to render:', error.message, info.componentStack?.split('\n')[1] || '');
  }

  componentDidMount() {
    window.addEventListener('hashchange', this.reset);
  }

  componentWillUnmount() {
    window.removeEventListener('hashchange', this.reset);
  }

  reset = () => {
    if (this.state.failed) this.setState({ failed: false });
  };

  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <div className="notice-view" role="alert">
        <h1 className="notice-view-title">This view could not be displayed</h1>
        <div className="notice-view-body">
          Something went wrong while rendering this page. The rest of the site is unaffected.
        </div>
        <a className="adv-back" href="#/">
          ← Back to overview
        </a>
      </div>
    );
  }
}
