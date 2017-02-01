package exp.bussiness;

public class AppExampleUseCases implements ExampleUseCases {

	public ExampleDao exampleDao;

	@Inject
	public AppExampleUseCases(@NonNull final ExampleDao exampleDao ) {
		this.exampleDao = exampleDao;
	}

	@Override
	public Example createExample(final ExampleDto exampleDto) throws GeneralBusinessErrorException {
		try {
			return exampleDao.createExample(exampleDto);
		} catch (Exception exception) {
			throw new GeneralBusinessErrorException(exception.getMessage());
		}
	}

	@Override
	public List<Example> getAllExamplesFiltered(final Long testId, final String begin, final String end, final String status) throws GeneralBusinessErrorException {
		try {
			return exampleDao.getAllExamplesFiltered(testId, begin, end, status);
		} catch (Exception exception) {
			throw new GeneralBusinessErrorException(exception.getMessage());
		}
	}

	@Override
	public Void testExample(final ExampleDto exampleDto) throws GeneralBusinessErrorException {
		try {
			return exampleDao.testExample(exampleDto);
		} catch (Exception exception) {
			throw new GeneralBusinessErrorException(exception.getMessage());
		}
	}

}