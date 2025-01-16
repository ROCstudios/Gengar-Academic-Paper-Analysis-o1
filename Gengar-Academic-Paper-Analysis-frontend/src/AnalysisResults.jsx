import { useState } from 'react';
import PropTypes from 'prop-types';

const ErrorCard = ({ error }) => (
  <div className="card bg-base-200">
    <div className="card-body">
      <h3 className="card-title text-error">{error.errorCategory}</h3>
      <div className="space-y-2">
        <div>
          <span className="font-medium">Issue: </span>
          <span>{error.issue}</span>
        </div>
        <div>
          <span className="font-medium">Implications: </span>
          <span>{error.implications}</span>
        </div>
        <div>
          <span className="font-medium">Recommendation: </span>
          <span>{error.recommendation}</span>
        </div>
      </div>
    </div>
  </div>
);

const SummaryStats = ({ data, errorCategories }) => (
  <div className="stats stats-vertical shadow w-full">
    {Object.entries(errorCategories).map(([key, label]) => (
      <div key={key} className="stat w-full">
        <div className="stat-title">{label}</div>
        <div className="stat-value">{data[key].errors.length}</div>
      </div>
    ))}
  </div>
);

const TabButton = ({ isActive, onClick, children }) => (
  <button 
    className={`tab flex items-center justify-center ${isActive ? 'tab-active' : ''}`}
    onClick={onClick}
  >
    {children}
  </button>
);

const Analysis = ({ data }) => {
  const [activeTab, setActiveTab] = useState('summary');

  const errorCategories = {
    calculation: 'Calculation',
    citation: 'Citation',
    data_inconsistencies: 'Data Inconsistencies',
    ethical: 'Ethical',
    formatting: 'Formatting',
    logical: 'Logical',
    methodical: 'Methodical'
  };

  return (
    <div className="bg-base-100 shadow-xl rounded-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">{data.summary.title}</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">Authors</p>
            <p className="font-medium">{data.summary.authors}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Published</p>
            <p className="font-medium">{data.summary.published}</p>
          </div>
          <div className="col-span-2">
            <p className="text-sm text-gray-600">Total Errors Found</p>
            <p className="text-2xl font-bold text-error">{data.summary.errorCount}</p>
          </div>
        </div>
      </div>

      <div className="tabs tabs-boxed mb-4">
        <TabButton 
          isActive={activeTab === 'summary'}
          onClick={() => setActiveTab('summary')}
          className="flex items-center justify-center"
        >
          Summary
        </TabButton>
        {Object.entries(errorCategories).map(([key, label]) => (
          data[key].errors.length > 0 && (
            <TabButton
              key={key}
              isActive={activeTab === key}
              onClick={() => setActiveTab(key)}
            > {label} </TabButton>
          )
        ))}
      </div>

      <div className="mt-4">
        {activeTab === 'summary' ? (
          <SummaryStats data={data} errorCategories={errorCategories} />
        ) : (
          <div className="space-y-4">
            {data[activeTab].errors.map((error, index) => (
              <ErrorCard key={index} error={error} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

ErrorCard.propTypes = {
  error: PropTypes.shape({
    errorCategory: PropTypes.string.isRequired,
    implications: PropTypes.string.isRequired,
    issue: PropTypes.string.isRequired,
    recommendation: PropTypes.string.isRequired
  }).isRequired
};

SummaryStats.propTypes = {
  data: PropTypes.object.isRequired,
  errorCategories: PropTypes.object.isRequired
};

TabButton.propTypes = {
  isActive: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired
};

Analysis.propTypes = {
  data: PropTypes.shape({
    calculation: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    citation: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    data_inconsistencies: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    ethical: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    formatting: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    logical: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    methodical: PropTypes.shape({ errors: PropTypes.array.isRequired }).isRequired,
    pdf_name: PropTypes.string.isRequired,
    summary: PropTypes.shape({
      authors: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      published: PropTypes.string.isRequired,
      errorCount: PropTypes.string.isRequired
    }).isRequired,
    timestamp: PropTypes.string.isRequired
  }).isRequired
};

export default Analysis;
